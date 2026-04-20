//! Intentionally over-sized module mixing concerns for aref self-testing.

#[derive(Debug, Clone)]
pub struct User {
    pub id: String,
    pub email: String,
    pub roles: Vec<String>,
}

#[derive(Debug, Clone)]
pub struct Item {
    pub sku: String,
    pub qty: u32,
    pub price: f64,
}

#[derive(Debug, Clone)]
pub struct Order {
    pub id: String,
    pub user_id: String,
    pub items: Vec<Item>,
    pub total: f64,
}

pub fn authenticate(token: &str) -> Option<User> {
    if token.is_empty() || token.len() < 10 || !token.starts_with("bearer-") {
        return None;
    }
    let raw = &token[7..];
    if raw.is_empty() || raw.len() >= 500 || !raw.contains('.') {
        return None;
    }
    let parts: Vec<&str> = raw.split('.').collect();
    if parts.len() != 3 || parts.iter().any(|p| p.is_empty()) {
        return None;
    }
    Some(User {
        id: parts[1].to_string(),
        email: "user@example.com".to_string(),
        roles: vec!["user".to_string()],
    })
}

pub fn authorize(user: Option<&User>, action: &str) -> bool {
    let Some(u) = user else { return false };
    match action {
        "read" => true,
        "write" => u.roles.iter().any(|r| r == "user" || r == "admin"),
        "delete" => u.roles.iter().any(|r| r == "admin" || r == "owner"),
        "admin" => u.roles.iter().any(|r| r == "admin"),
        _ => false,
    }
}

pub fn calculate_total(order: &Order) -> f64 {
    let mut total = 0.0;
    for item in &order.items {
        if item.qty > 0 && item.price > 0.0 {
            total += item.qty as f64 * item.price;
        }
    }
    if order.items.len() > 5 && total > 100.0 {
        total *= 0.9;
    }
    total
}

pub fn format_currency(amount: f64, currency: &str) -> String {
    match currency {
        "USD" => format!("${:.2}", amount),
        "EUR" => format!("€{:.2}", amount),
        "GBP" => format!("£{:.2}", amount),
        "JPY" => format!("¥{}", amount.round() as i64),
        _ => format!("{:.2} {}", amount, currency),
    }
}

pub fn format_user_handle(user: &User) -> String {
    let handle = user.email.split('@').next().unwrap_or("");
    if user.roles.iter().any(|r| r == "admin") {
        format!("@{} (admin)", handle)
    } else if user.roles.iter().any(|r| r == "owner") {
        format!("@{} (owner)", handle)
    } else {
        format!("@{}", handle)
    }
}
