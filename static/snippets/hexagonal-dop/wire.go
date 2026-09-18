// dop-core/internal/app/wire.go (excerpt)
//
// Package app is the COMPOSITION ROOT: where the ports receive their adapters.
// It is the only place in the system that knows both ends. The domain knows only
// the ports; the adapters know only their technology. The choice happens here,
// by configuration — never through a conditional scattered across the code.
package app

// Deps gathers everything the use cases need — always as a PORT, never as an
// adapter's concrete type.
type Deps struct {
	Pool     *pgxpool.Pool
	Bus      ports.EventBus
	Secrets  ports.SecretStore
	Objects  ports.ObjectStore
	Identity ports.IdentityProvider
	Launcher ports.SandboxLauncher
	Runner   ports.VerificationRunner
	Mailer   ports.Mailer
	SMS      ports.SMSer
	Repos    ports.ProjectRepository
	Cfg      *config.Config
}

func Build(ctx context.Context, cfg *config.Config) (*Deps, func(), error) {
	// ...pool and bus...

	// ── choosing the adapters by configuration ──
	var secrets ports.SecretStore
	switch cfg.SecretBackend {
	case "memory":
		secrets = secretstore.NewMemory()
	case "gcp":
		// The port's guarantee 1 (read-after-write) is NOT deliverable on real
		// GCP as-is. The adapter confirms by version number, which is strong,
		// and then waits for the `latest` alias to catch up; if it does not
		// converge, it refuses with KindUnavailable instead of returning "it
		// does not exist" for a credential that was just written.
		gcp, err := secretstore.NewGCP(ctx, secretstore.GCPConfig{
			ProjectID:   cfg.SecretProject,
			Endpoint:    cfg.SecretEndpoint,
			Propagation: cfg.SecretPropagation,
		})
		if err != nil {
			return nil, nil, err
		}
		closers = append(closers, gcp.Close)
		secrets = gcp
	default: // k8s — used locally and in self-hosted; there is no Secret Manager emulator
		secrets = secretstore.NewK8s(secretstore.K8sConfig{
			APIServer: cfg.K8sAPIServer,
			Token:     cfg.K8sToken,
			Namespace: cfg.K8sNamespace,
		})
	}

	// The executor is also a port with two REAL adapters: Docker for local
	// development with no cluster, k8s for the execution cluster. Both pass
	// the same contract suite.
	var launcher ports.SandboxLauncher
	switch cfg.SandboxBackend {
	case "docker":
		launcher = sandbox.NewDocker(sandbox.DockerConfig{Socket: cfg.DockerSocket})
	default:
		launcher = sandbox.NewK8s(/* ... */)
	}

	// ...identity (firebase | oidc), mailer (smtp | sendgrid), sms (twilio | zenvia)...
	return &Deps{Secrets: secrets, Launcher: launcher /* ... */}, cleanup, nil
}
