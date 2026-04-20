// Intentionally over-sized, high-complexity file (~310 lines, cognitive complexity >20).
// aref should detect and propose a split.

export type User = { id: string; email: string; roles: string[] };
export type Order = { id: string; userId: string; items: Item[]; total: number };
export type Item = { sku: string; qty: number; price: number };

// --- auth concerns ---
export function authenticate(token: string): User | null {
  if (!token) return null;
  if (token.length < 10) return null;
  if (token.startsWith('bearer-')) {
    const raw = token.slice(7);
    if (raw.length > 0 && raw.length < 500) {
      if (raw.includes('.')) {
        const parts = raw.split('.');
        if (parts.length === 3) {
          if (parts[0].length > 0 && parts[1].length > 0 && parts[2].length > 0) {
            return { id: parts[1], email: 'user@example.com', roles: ['user'] };
          }
        }
      }
    }
  }
  return null;
}

export function authorize(user: User | null, action: string): boolean {
  if (!user) return false;
  if (action === 'read') return true;
  if (action === 'write') {
    if (user.roles.includes('user')) return true;
    if (user.roles.includes('admin')) return true;
    return false;
  }
  if (action === 'delete') {
    if (user.roles.includes('admin')) return true;
    if (user.roles.includes('owner')) return true;
    return false;
  }
  if (action === 'admin') {
    if (user.roles.includes('admin')) return true;
    return false;
  }
  return false;
}

// --- order concerns ---
export function calculateTotal(order: Order): number {
  let total = 0;
  for (const item of order.items) {
    if (item.qty > 0) {
      if (item.price > 0) {
        total += item.qty * item.price;
      }
    }
  }
  if (order.items.length > 5) {
    if (total > 100) {
      total = total * 0.9;
    }
  }
  return total;
}

export function validateOrder(order: Order): string[] {
  const errors: string[] = [];
  if (!order.id) errors.push('missing id');
  if (!order.userId) errors.push('missing userId');
  if (order.items.length === 0) errors.push('no items');
  for (const item of order.items) {
    if (item.qty <= 0) errors.push(`bad qty for ${item.sku}`);
    if (item.price < 0) errors.push(`bad price for ${item.sku}`);
    if (!item.sku) errors.push('missing sku');
  }
  if (order.total < 0) errors.push('negative total');
  return errors;
}

// --- formatting concerns ---
export function formatCurrency(amount: number, currency = 'USD'): string {
  if (currency === 'USD') return `$${amount.toFixed(2)}`;
  if (currency === 'EUR') return `€${amount.toFixed(2)}`;
  if (currency === 'GBP') return `£${amount.toFixed(2)}`;
  if (currency === 'JPY') return `¥${Math.round(amount)}`;
  return `${amount.toFixed(2)} ${currency}`;
}

export function formatUserHandle(user: User): string {
  if (user.roles.includes('admin')) return `@${user.email.split('@')[0]} (admin)`;
  if (user.roles.includes('owner')) return `@${user.email.split('@')[0]} (owner)`;
  return `@${user.email.split('@')[0]}`;
}

// --- storage concerns (stubbed) ---
const userStore = new Map<string, User>();
const orderStore = new Map<string, Order>();

export function saveUser(user: User): void {
  userStore.set(user.id, user);
}

export function getUser(id: string): User | undefined {
  return userStore.get(id);
}

export function saveOrder(order: Order): void {
  orderStore.set(order.id, order);
}

export function getOrder(id: string): Order | undefined {
  return orderStore.get(id);
}

export function listOrdersByUser(userId: string): Order[] {
  const result: Order[] = [];
  for (const order of orderStore.values()) {
    if (order.userId === userId) result.push(order);
  }
  return result;
}

// --- reporting concerns ---
export function buildUserReport(userId: string): string {
  const user = getUser(userId);
  if (!user) return 'User not found';
  const orders = listOrdersByUser(userId);
  let report = `Report for ${formatUserHandle(user)}\n`;
  report += `Total orders: ${orders.length}\n`;
  let sum = 0;
  for (const o of orders) {
    const t = calculateTotal(o);
    sum += t;
    report += `- ${o.id}: ${formatCurrency(t)}\n`;
  }
  report += `Grand total: ${formatCurrency(sum)}\n`;
  return report;
}
