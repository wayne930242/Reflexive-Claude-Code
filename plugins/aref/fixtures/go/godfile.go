// Package fixture is an intentionally over-sized package mixing concerns for aref self-testing.
package fixture

import "fmt"

type User struct {
	ID    string
	Email string
	Roles []string
}

type Item struct {
	SKU   string
	Qty   int
	Price float64
}

type Order struct {
	ID     string
	UserID string
	Items  []Item
	Total  float64
}

func Authenticate(token string) *User {
	if token == "" || len(token) < 10 || token[:7] != "bearer-" {
		return nil
	}
	raw := token[7:]
	if raw == "" || len(raw) >= 500 {
		return nil
	}
	parts := splitDot(raw)
	if len(parts) != 3 {
		return nil
	}
	for _, p := range parts {
		if p == "" {
			return nil
		}
	}
	return &User{ID: parts[1], Email: "user@example.com", Roles: []string{"user"}}
}

func splitDot(s string) []string {
	var out []string
	start := 0
	for i := 0; i < len(s); i++ {
		if s[i] == '.' {
			out = append(out, s[start:i])
			start = i + 1
		}
	}
	out = append(out, s[start:])
	return out
}

func Authorize(user *User, action string) bool {
	if user == nil {
		return false
	}
	switch action {
	case "read":
		return true
	case "write":
		return hasRole(user, "user") || hasRole(user, "admin")
	case "delete":
		return hasRole(user, "admin") || hasRole(user, "owner")
	case "admin":
		return hasRole(user, "admin")
	}
	return false
}

func hasRole(u *User, role string) bool {
	for _, r := range u.Roles {
		if r == role {
			return true
		}
	}
	return false
}

func CalculateTotal(order Order) float64 {
	total := 0.0
	for _, item := range order.Items {
		if item.Qty > 0 && item.Price > 0 {
			total += float64(item.Qty) * item.Price
		}
	}
	if len(order.Items) > 5 && total > 100 {
		total *= 0.9
	}
	return total
}

func FormatCurrency(amount float64, currency string) string {
	switch currency {
	case "USD":
		return fmt.Sprintf("$%.2f", amount)
	case "EUR":
		return fmt.Sprintf("€%.2f", amount)
	case "GBP":
		return fmt.Sprintf("£%.2f", amount)
	case "JPY":
		return fmt.Sprintf("¥%d", int(amount))
	}
	return fmt.Sprintf("%.2f %s", amount, currency)
}
