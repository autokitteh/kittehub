package main

import (
	"context"
	"errors"
	"log"

	"connectrpc.com/connect"

	apiv1 "github.com/autokitteh/kittehub/deploysentry/go/gen"
)

type val struct {
	v string
	r int32
}

type handler struct{ deploys map[string]val }

func (h *handler) Deploy(_ context.Context, req *connect.Request[apiv1.DeployRequest]) (*connect.Response[apiv1.DeployResponse], error) {
	log.Printf("deploy %s#%s", req.Msg.Svc, req.Msg.Version)

	h.deploys[req.Msg.Svc] = val{v: req.Msg.Version, r: 0}

	return connect.NewResponse(&apiv1.DeployResponse{}), nil
}

func (h *handler) SetRatio(_ context.Context, req *connect.Request[apiv1.SetRatioRequest]) (*connect.Response[apiv1.SetRatioResponse], error) {
	if _, ok := h.deploys[req.Msg.Svc]; !ok {
		return nil, connect.NewError(connect.CodeNotFound, errors.New("deploy not found"))
	}

	log.Printf("set ratio %s#%s to %d", req.Msg.Svc, req.Msg.Version, req.Msg.Ratio)

	h.deploys[req.Msg.Svc] = val{v: req.Msg.Version, r: req.Msg.Ratio}

	return connect.NewResponse(&apiv1.SetRatioResponse{}), nil
}

func (h *handler) get(svc string) val {
	return h.deploys[svc]
}

func (h *handler) Get(_ context.Context, req *connect.Request[apiv1.GetRequest]) (*connect.Response[apiv1.GetResponse], error) {
	v := h.get(req.Msg.Svc)

	return connect.NewResponse(&apiv1.GetResponse{Version: v.v, Ratio: v.r}), nil
}

func newHandler() *handler { return &handler{deploys: make(map[string]val)} }
