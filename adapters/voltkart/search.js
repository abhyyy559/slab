import { cli, Strategy } from '@agentrhq/webcmd/registry';

cli({
  site: 'voltkart',
  name: 'search',
  description: 'Search VoltKart phones; return in-stock products within budget and RAM floor',
  access: 'read',
  example: 'webcmd voltkart search --base http://127.0.0.1:8000 --max-price 20000 --min-ram 8 -f json',
  domain: '127.0.0.1:8000',
  strategy: Strategy.UI,
  browser: true,
  args: [
    { name: 'base', type: 'str', default: 'http://127.0.0.1:8000', help: 'Mock server base URL' },
    { name: 'max-price', type: 'int', default: 20000, help: 'Max price in Rs' },
    { name: 'min-ram', type: 'int', default: 8, help: 'Min RAM in GB' },
  ],
  columns: ['name', 'price', 'ram'],
  func: async (page, kwargs) => {
    await page.goto(kwargs.base + '/site_a/search.html', { waitUntil: 'domcontentloaded' });
    return await page.evaluate((args) => {
      document.querySelector('[data-testid="max-price"]').value = String(args.maxPrice);
      document.querySelector('[data-testid="min-ram"]').value = String(args.minRam);
      document.querySelector('[data-testid="apply-filter"]').click();
      return new Promise((resolve) => setTimeout(() => {
        resolve([...document.querySelectorAll('[data-testid="product-card"]')]
          .filter((c) => c.style.display !== 'none')
          .map((c) => ({ name: c.dataset.name, price: parseInt(c.dataset.price, 10), ram: parseInt(c.dataset.ram, 10) })));
      }, 600));
    }, { maxPrice: kwargs['max-price'], minRam: kwargs['min-ram'] });
  },
});
