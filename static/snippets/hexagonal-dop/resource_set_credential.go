// dop-core/internal/domain/resource/service.go (excerpt)
//
// The use case that puts a third party's key into the vault. Note what the
// domain knows: a SecretRef built from its own identifiers, and four verbs.
// It does not know whether the vault is Secret Manager, a k8s Secret or a map.
//
// The order is vault first, row second: if the database fails, an orphan
// secret with no pointer is left behind (inert, and overwritten on the next
// attempt); the reverse order would leave the row claiming a credential that
// does not exist, and execution would fail far from here, with no explanation.
func (s *Service) SetCredential(ctx context.Context, resourceID string, secret []byte) (string, error) {
	a, err := s.who(ctx)
	if err != nil {
		return "", err
	}
	if len(secret) == 0 {
		return "", errs.Invalid("empty credential").WithCode(KeyCredentialEmpty, nil)
	}
	// The second factor's gate: it comes AFTER the cheap validation and BEFORE
	// the authorization, so that a caller with no session does not learn which
	// resources exist.
	if err := s.requireStepUp(ctx); err != nil {
		return "", err
	}
	r, err := s.authorize(ctx, a, resourceID, LevelManage)
	if err != nil {
		return "", err
	}
	if !r.HasCredential() {
		return "", errs.Precondition("a resource of kind %q has no credential", r.Kind).
			WithCode(KeyKindHasNoCredential, map[string]any{"kind": string(r.Kind)})
	}

	if err := s.secrets.Put(ctx, SecretRefFor(a.accountID, r.ID), ports.SecretValue(secret)); err != nil {
		return "", errs.Wrap(errs.KindUnavailable, err,
			"failed to store the credential of resource %s", r.ID)
	}
	saved, err := s.repo.SetCredentialRef(ctx, a.accountID, r.ID, CredentialRef(a.accountID, r.ID))
	if err != nil {
		return "", err
	}
	return saved.CredentialRef, nil
}

// SecretRefFor is the domain's side of the reference: its own identifiers,
// nothing about where the secret physically lives.
func SecretRefFor(accountID, resourceID string) ports.SecretRef {
	return ports.SecretRef{
		AccountID: accountID,
		Kind:      CredentialKind,
		OwnerID:   resourceID,
	}
}
