// dop-core/internal/domain/ports/ports.go (excerpt)
//
// Package ports declares the infrastructure PORTS, in the domain's language.
// The domain defines the port with the narrowest surface it needs; vendor
// adapters live in internal/adapter and are chosen by configuration at the
// composition root. No SDK crosses this boundary, and any capability that
// does not map across adapters stays OUT of the port.
package ports

// SecretRef is a LOGICAL, opaque reference: only the adapter knows how to
// resolve it (a path in Secret Manager, a Secret name in k8s). The domain never
// knows a path, a namespace or a secret name.
type SecretRef struct {
	AccountID string
	Kind      string // integration_credential
	OwnerID   string
}

// SecretValue is opaque by construction: with no useful String(), it does not
// serialize into a log.
type SecretValue []byte

func (SecretValue) String() string { return "***" }

// SecretStore — four operations and nothing more.
//
// Guarantees verified by the contract suite, in EVERY adapter:
//  1. read-after-write: Put followed by Get returns the same value, immediately;
//  2. Get of a missing reference returns (nil, nil) — not an error;
//  3. Delete is idempotent;
//  4. Put over an existing reference replaces it;
//  5. isolation: a reference of account A never resolves a secret of account B;
//  6. the value never appears in a log, an error or a stack trace.
//
// Versioning stays OUT of the port: Secret Manager has versions, a k8s Secret
// is flat. A capability that does not map does not get in.
type SecretStore interface {
	Put(ctx context.Context, ref SecretRef, v SecretValue) error
	Get(ctx context.Context, ref SecretRef) (SecretValue, error)
	Delete(ctx context.Context, ref SecretRef) error
	Exists(ctx context.Context, ref SecretRef) (bool, error)
}
