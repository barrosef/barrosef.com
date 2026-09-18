// dop-core/internal/adapter/secretstore/gcp.go (excerpt)
//
// Put → AddSecretVersion, confirmed by VERSION NUMBER (strongly consistent),
//       then waiting for the `latest` alias (eventual), then destroying the
//       older versions' material.
// Get → AccessSecretVersion on ".../versions/latest".
//
// Why Get reads `latest` and not a named version: the port has nowhere to keep
// a version number — SecretRef is flat and the domain knows no version.

// awaitLatest waits for the `latest` alias to reach the written version.
//
// Without this, "write and return" would be read-after-write only on the
// emulator: on real GCP the alias is eventually consistent, and a Get right
// after the Put would return (nil, nil) — which through the port means "it does
// not exist". A just-written credential would show up as absent, in silence.
func (g *GCP) awaitLatest(ctx context.Context, id string, want int64) error {
	deadline := time.Now().Add(g.propagation) // SECRET_PROPAGATION_SECONDS, 30 s by default
	wait := 25 * time.Millisecond
	for {
		resp, err := g.client.AccessSecretVersion(ctx, &secretmanagerpb.AccessSecretVersionRequest{
			Name: g.secretName(id) + "/versions/latest",
		})
		switch {
		case err == nil:
			got, verr := versionNumber(resp.GetName())
			if verr != nil {
				return verr
			}
			// >= and not ==: another concurrent Put may already have gone
			// ahead, and in that case propagation has more than caught up.
			if got >= want {
				return nil
			}
		case status.Code(err) == codes.NotFound, status.Code(err) == codes.FailedPrecondition:
			// not propagated yet — exactly the case this wait covers
		default:
			return wrapGCP(err, "failed to confirm the secret's visibility")
		}

		if !time.Now().Before(deadline) {
			// Refusing is the part that matters: a Put that returns success
			// while the following Get says "it does not exist" is worse than
			// a Put that fails.
			return errs.New(errs.KindUnavailable,
				"Secret Manager did not make version %d visible through `latest` within %s: "+
					"the write was accepted, but read-after-write was not confirmed",
				want, g.propagation)
		}
		select {
		case <-ctx.Done():
			return errs.Wrap(errs.KindUnavailable, ctx.Err(),
				"context ended before confirming the secret's visibility")
		case <-time.After(wait):
		}
		if wait < time.Second {
			wait *= 2
		}
	}
}
