package main

import (
	"encoding/json"
	"log"
	"net/http"

	"connectrpc.com/grpcreflect"
	"github.com/autokitteh/kittehub/deploysentry/go/gen/apiv1connect"
	"golang.org/x/net/http2"
	"golang.org/x/net/http2/h2c"
)

type key struct{ svc, version string }

var stats = map[key]int32{
	{svc: "svc1", version: "v1"}: 0,
	{svc: "svc1", version: "v2"}: 10,
	{svc: "svc1", version: "v3"}: 20,
}

func main() {
	mux := http.NewServeMux()

	h := newHandler()

	mux.Handle(apiv1connect.NewDeploySentryServiceHandler(h))

	mux.Handle(grpcreflect.NewHandlerV1(
		grpcreflect.NewStaticReflector(apiv1connect.DeploySentryServiceName),
	))

	mux.Handle("/check", http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		svc := r.URL.Query().Get("svc")

		v := h.get(svc)

		total := int32(float32(stats[key{svc: svc, version: v.v}]) * float32(v.r) / float32(100))

		w.Header().Set("Content-Type", "application/json")
		if err := json.NewEncoder(w).Encode(map[string]int32{"error_rate": total}); err != nil {
			log.Printf("json encode: %v", err)
		}

		log.Printf("check %s: %d errors", svc, total)
	}))

	log.Print("Starting HTTP server on port 8080")

	srv := &http.Server{
		Addr: ":8080",
		Handler: h2c.NewHandler(
			mux,
			&http2.Server{},
		),
	}

	if err := srv.ListenAndServe(); err != nil {
		log.Fatalf("HTTP listen and serve: %v", err)
	}
}
