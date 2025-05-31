package url

func ProcessCodeforces(url string) (map[string]string, error) {
	return map[string]string{
		"site": "codeforces",
		"url":  url,
		"info": "Codeforces question processed",
	}, nil
}
