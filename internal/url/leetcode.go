package url

import (
	"bytes"
	"encoding/json"
	"errors"
	"fmt"
	"io"
	"net/http"
	"regexp"
	"strings"

	"github.com/ab1nv/lantern/internal/core" // adjust import path to match your module
)

type leetcodeResponse struct {
	Data struct {
		Question struct {
			ID         string `json:"questionFrontendId"`
			Title      string `json:"title"`
			Difficulty string `json:"difficulty"`
			TopicTags  []struct {
				Name string `json:"name"`
			} `json:"topicTags"`
		} `json:"question"`
	} `json:"data"`
}

var headers = map[string]string{
	"User-Agent":   "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
	"Accept":       "application/json",
	"Content-Type": "application/json",
	"Origin":       "https://leetcode.com",
	"Referer":      "https://leetcode.com/",
}

func extractSlug(url string) (string, error) {
	re := regexp.MustCompile(`problems/([^/]+)`)
	matches := re.FindStringSubmatch(url)
	if len(matches) < 2 {
		return "", errors.New("could not extract slug from URL")
	}
	return matches[1], nil
}

// baseDir is the watched directory (e.g., "problemset"), ext is the file extension (e.g., ".py")
func ProcessLeetCode(url string, baseDir string, ext string) (map[string]string, error) {
	slug, err := extractSlug(url)
	if err != nil {
		return nil, err
	}

	query := map[string]interface{}{
		"query": `
		query getQuestionDetails($titleSlug: String!) {
			question(titleSlug: $titleSlug) {
				questionFrontendId
				title
				difficulty
				topicTags { name }
			}
		}`,
		"variables": map[string]string{
			"titleSlug": slug,
		},
	}

	jsonData, err := json.Marshal(query)
	if err != nil {
		return nil, err
	}

	req, err := http.NewRequest("POST", "https://leetcode.com/graphql", bytes.NewBuffer(jsonData))
	if err != nil {
		return nil, err
	}
	for k, v := range headers {
		req.Header.Set(k, v)
	}

	client := &http.Client{}
	resp, err := client.Do(req)
	if err != nil {
		return nil, err
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		return nil, fmt.Errorf("GraphQL request failed with status %d", resp.StatusCode)
	}

	body, err := io.ReadAll(resp.Body)
	if err != nil {
		return nil, err
	}

	var parsed leetcodeResponse
	if err := json.Unmarshal(body, &parsed); err != nil {
		return nil, err
	}

	q := parsed.Data.Question
	if q.Title == "" {
		return nil, errors.New("invalid or missing data in LeetCode response")
	}

	topics := make([]string, len(q.TopicTags))
	for i, tag := range q.TopicTags {
		topics[i] = tag.Name
	}

	// 👇 Auto-create files in watched directory
	meta := core.QuestionMeta{
		QuestionID:    q.ID,
		QuestionSlug:  slug,
		QuestionTitle: q.Title,
	}
	if err := core.CreateLeetCodeFiles(baseDir, meta, ext); err != nil {
		return nil, fmt.Errorf("failed to create local files: %w", err)
	}

	return map[string]string{
		"question_id":    q.ID,
		"question_title": q.Title,
		"question_slug":  slug,
		"difficulty":     q.Difficulty,
		"topic_tags":     strings.Join(topics, ", "),
		"url":            url,
	}, nil
}
