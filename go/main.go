package main

import (
    "fmt"
    "crypto/rand"
    "encoding/hex"
    "net/http"
)

var token,_ = randToken(3)

func main() {
    http.HandleFunc("/", HelloServer)
    http.ListenAndServe(":5000", nil)
}

func HelloServer(w http.ResponseWriter, r *http.Request) {
	fmt.Fprintf(w, "<h1 style=color:#%s>Hello golang</h1><h2>ID: %s</h2>", token, token)
}

func randToken(n int) (string, error) {
	bytes := make([]byte, n)
	if _, err := rand.Read(bytes); err != nil {
		return "", err
	}
	return hex.EncodeToString(bytes), nil
}
