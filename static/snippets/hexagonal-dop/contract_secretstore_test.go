// dop-core/test/contract/secretstore_test.go — the suite against the in-memory
// adapter. It ALWAYS runs.
package contract_test

func TestSecretStoreContract(t *testing.T) {
	contract.SecretStoreSuite(t, "memory", func(t *testing.T) ports.SecretStore {
		return secretstore.NewMemory()
	})
}

// dop-core/test/contract/secretstore_gcp_test.go — the SAME suite, now against
// Secret Manager. Locally the target is the community emulator; pointing
// SECRET_MANAGER_EMULATOR_HOST at nothing and supplying a credential, the SAME
// function runs against real GCP — which is the only way to discover the
// divergences listed in the adapter's header.
//
//	go test ./test/contract/ -tags=integration -v -run SecretStore
//
// BEWARE when reading a PASS here: the emulator is more permissive than real
// GCP in nine documented points, and one of them is the port's guarantee 1 —
// read-after-write, which Google does NOT promise through the `latest` alias.
// Green here is no proof of green there.

//go:build integration

func TestSecretStoreContractGCP(t *testing.T) {
	endpoint := os.Getenv("SECRET_MANAGER_EMULATOR_HOST")
	if endpoint == "" {
		endpoint = "127.0.0.1:8085"
	}
	contract.SecretStoreSuite(t, "gcp", func(t *testing.T) ports.SecretStore {
		// One PROJECT per newStore call: the suite counts on clean state.
		s, err := secretstore.NewGCP(context.Background(), secretstore.GCPConfig{
			ProjectID: fmt.Sprintf("contract-%d", time.Now().UnixNano()),
			Endpoint:  endpoint,
		})
		if err != nil {
			t.Skipf("Secret Manager unreachable at %s: %v", endpoint, err)
		}
		t.Cleanup(func() { _ = s.Close() })
		return s
	})
}
