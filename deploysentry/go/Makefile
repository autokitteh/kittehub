.PHONY: srv
srv: gen
	go build .

.PHONY: gen
gen:
	rm -fR gen
	buf generate 
