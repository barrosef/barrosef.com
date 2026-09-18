// dop-core/test/contract/secretstore.go (excerpt)
//
// Package contract carries the ports' CONTRACT tests. A port with a single
// adapter is guesswork. The same set runs against EVERY adapter — in-memory,
// k8s, GCP Secret Manager — and it is what guarantees substitutability in
// fact, not in intention.
package contract

// SecretStoreSuite verifies the six guarantees documented on the port.
func SecretStoreSuite(t *testing.T, name string, newStore func(t *testing.T) ports.SecretStore) {
	t.Run(name, func(t *testing.T) {
		// UNIQUE accounts per run, and not fixed literals.
		//
		// The first version used fixed "acct-a"/"acct-b", and the suite passed —
		// against the in-memory double, where `newStore` returns a fresh vault
		// on every subtest. Against a REAL backend, `newStore` returns a new
		// client for the SAME vault, and the secret written in subtest 1 made
		// the `Exists` subtest fail by finding what it had left behind itself.
		//
		// It was the suite written on top of the double: it verified the port,
		// but carried along an assumption only the double satisfied.
		id := fmt.Sprintf("%d-%d", time.Now().UnixNano(), refSeq.Add(1))
		refA := ports.SecretRef{AccountID: "acct-a-" + id, Kind: "integration_credential", OwnerID: "res-1"}
		refB := ports.SecretRef{AccountID: "acct-b-" + id, Kind: "integration_credential", OwnerID: "res-1"}
		val := ports.SecretValue("super-secret-token")

		cleanup := newStore(t)
		t.Cleanup(func() {
			_ = cleanup.Delete(context.Background(), refA)
			_ = cleanup.Delete(context.Background(), refB)
		})

		t.Run("1_immediate_read_after_write", func(t *testing.T) {
			s := newStore(t)
			ctx := context.Background()
			if err := s.Put(ctx, refA, val); err != nil {
				t.Fatalf("Put: %v", err)
			}
			got, err := s.Get(ctx, refA)
			if err != nil {
				t.Fatalf("Get: %v", err)
			}
			if !bytes.Equal(got, val) {
				t.Fatalf("value differs: %q != %q", got, val)
			}
		})

		t.Run("2_absent_returns_nil_with_no_error", func(t *testing.T) {
			s := newStore(t)
			got, err := s.Get(context.Background(),
				ports.SecretRef{AccountID: "acct-x", Kind: "integration_credential", OwnerID: "does-not-exist"})
			if err != nil {
				t.Fatalf("expected nil with no error, got error: %v", err)
			}
			if got != nil {
				t.Fatalf("expected nil, got %q", got)
			}
		})

		t.Run("3_idempotent_delete", func(t *testing.T) {
			s := newStore(t)
			ctx := context.Background()
			_ = s.Put(ctx, refA, val)
			if err := s.Delete(ctx, refA); err != nil {
				t.Fatalf("1st Delete: %v", err)
			}
			if err := s.Delete(ctx, refA); err != nil {
				t.Fatalf("the 2nd Delete should be harmless: %v", err)
			}
		})

		// 4_put_replaces, 5_isolation_between_accounts, 6_value_never_logged ...
	})
}
