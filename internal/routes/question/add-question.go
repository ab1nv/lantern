package routes

import (
	"encoding/json"
	"net/http"
	"strings"

	inturl "github.com/ab1nv/lantern/internal/url"
	"github.com/go-chi/chi/v5"
)

func RegisterQuestionRoutes(r chi.Router) {
	r.Post("/add-question", AddQuestionHandler)
}

func AddQuestionHandler(w http.ResponseWriter, r *http.Request) {
	urlParam := r.URL.Query().Get("url")
	if urlParam == "" {
		http.Error(w, "Missing 'url' parameter", http.StatusBadRequest)
		return
	}

	normalized, err := inturl.NormalizeURL(urlParam)
	if err != nil {
		http.Error(w, "Invalid URL: "+err.Error(), http.StatusBadRequest)
		return
	}

	var resp interface{}
	switch {
	case normalizedContains(normalized, "leetcode.com"):
		resp, err = inturl.ProcessLeetCode(normalized, "problemset", ".py")
	case normalizedContains(normalized, "codeforces.com"):
		resp, err = inturl.ProcessCodeforces(normalized)
	default:
		http.Error(w, "Unsupported platform", http.StatusBadRequest)
		return
	}

	if err != nil {
		http.Error(w, "Failed to process: "+err.Error(), http.StatusInternalServerError)
		return
	}

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(resp)
}

func normalizedContains(u, needle string) bool {
	return strings.Contains(strings.ToLower(u), needle)
}
