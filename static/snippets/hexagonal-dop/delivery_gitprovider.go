// dop-core/internal/domain/delivery/repository.go (excerpt)
//
// A DOMAIN PROVIDER port: it lives in the delivery domain, not in the shared
// ports package, because it is the delivery domain's vocabulary — a pull
// request, a rebase, a merge — and nothing else needs it.
package delivery

type GitProvider interface {
	OpenPullRequest(ctx context.Context, spec OpenPRSpec) (ProviderPR, error)
	Rebase(ctx context.Context, spec RebaseSpec) (RebaseResult, error)
	Merge(ctx context.Context, spec MergeSpec) (MergeResult, error)
	// HasNativeQueue says whether the provider has a merge queue of its own
	// (GitHub's, GitLab's merge trains). DOP's queue orchestrates on top and
	// covers who does not.
	HasNativeQueue(ctx context.Context, repoExternalID string) (bool, error)
}

// GitProviders resolves WHICH provider serves a repository.
//
// It is not a boot-time choice, like SecretStore or EventBus: the provider
// belongs to the REPOSITORY, and that is precisely why `ProjectRepo` carries an
// `IntegrationID` — a project with one repo on GitHub and another on GitLab has
// to be representable. A single provider chosen by configuration would make
// that impossible, silently.
//
// Whoever implements it also resolves the CREDENTIAL, in the vault — which is
// why the port returns a ready `GitProvider`, and no git adapter knows the vault.
type GitProviders interface {
	For(ctx context.Context, accountID, repoID string) (GitProvider, error)
}
