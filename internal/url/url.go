package url

import (
	"errors"
	"net/url"
	"strings"
)

// NormalizeURL parses and normalizes the input URL string:
// - https scheme
// - lowercase hostname
// - no trailing slashes
// - no fragments
func NormalizeURL(raw string) (string, error) {
	if raw == "" {
		return "", errors.New("empty URL")
	}

	if !strings.HasPrefix(raw, "http://") && !strings.HasPrefix(raw, "https://") {
		raw = "https://" + raw
	}

	parsed, err := url.Parse(raw)
	if err != nil {
		return "", err
	}

	parsed.Scheme = "https"
	parsed.Host = strings.ToLower(parsed.Host)
	parsed.Fragment = ""
	parsed.Path = strings.TrimRight(parsed.Path, "/")

	return parsed.String(), nil
}
