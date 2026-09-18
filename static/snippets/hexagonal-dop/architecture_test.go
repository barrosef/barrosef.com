// dop-core/test/contract/architecture_test.go (excerpt)
package contract_test

// The frontier that holds the architecture up: internal/domain must not
// import internal/adapter, nor any vendor SDK.
//
// This is a TEST, not a convention in the README — it is what makes the
// frontier survive time. Whoever tries to violate it breaks the build.
func TestTheDomainDoesNotImportInfrastructure(t *testing.T) {
	root := repoRoot(t)
	domainDir := filepath.Join(root, "internal", "domain")

	forbidden := []string{
		"/internal/adapter",      // the central rule
		"google.golang.org/grpc", // the protocol belongs to the edge
		"github.com/jackc/pgx",   // the database is an adapter
		"github.com/nats-io",     // the broker is an adapter
		"cloud.google.com/go",    // a vendor SDK
		"k8s.io/client-go",       // likewise
	}

	var violations []string
	err := filepath.Walk(domainDir, func(path string, info os.FileInfo, err error) error {
		if err != nil || info.IsDir() || !strings.HasSuffix(path, ".go") {
			return err
		}
		fset := token.NewFileSet()
		f, err := parser.ParseFile(fset, path, nil, parser.ImportsOnly)
		if err != nil {
			return err
		}
		rel, _ := filepath.Rel(root, path)
		for _, imp := range f.Imports {
			p := strings.Trim(imp.Path.Value, `"`)
			for _, banned := range forbidden {
				if strings.Contains(p, banned) {
					violations = append(violations,
						rel+" imports "+p+" (forbidden: "+banned+")")
				}
			}
		}
		return nil
	})
	if err != nil {
		t.Fatalf("the sweep failed: %v", err)
	}

	if len(violations) > 0 {
		t.Errorf("the domain↔infrastructure frontier was violated in %d place(s):", len(violations))
		for _, v := range violations {
			t.Errorf("  • %s", v)
		}
		t.Error("\ninternal/domain declares PORTS; adapters live in internal/adapter " +
			"and are chosen in the composition root (internal/app).")
	}
}

// The composition root is the ONLY place allowed to know both ends: anything
// under internal/ that is not internal/app or internal/adapter must not
// import an adapter package.
func TestOnlyAppKnowsTheAdapters(t *testing.T) { /* same sweep, other rule */ }
