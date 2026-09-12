import { cli, Strategy } from '@agentrhq/webcmd/registry';

cli({
  site: 'swiftship',
  name: 'check',
  description: 'Check SwiftShip 3-day delivery availability for a PIN code',
  access: 'read',
  example: 'webcmd swiftship check --base http://127.0.0.1:8000 --pin 500001 -f json',
  domain: '127.0.0.1:8000',
  strategy: Strategy.UI,
  browser: true,
  args: [
    { name: 'base', type: 'str', default: 'http://127.0.0.1:8000', help: 'Mock server base URL' },
    { name: 'pin', type: 'str', default: '500001', help: 'Destination PIN code' },
  ],
  columns: ['pin', 'status'],
  func: async (page, kwargs) => {
    await page.goto(kwargs.base + '/site_b/check.html', { waitUntil: 'domcontentloaded' });
    return await page.evaluate((args) => {
      document.querySelector('[data-testid="pin-input"]').value = String(args.pin);
      document.querySelector('[data-testid="check-button"]').click();
      return new Promise((resolve) => setTimeout(() => {
        resolve([{ pin: String(args.pin),
                   status: document.querySelector('[data-testid="delivery-status"]').textContent.trim() }]);
      }, 600));
    }, { pin: kwargs.pin });
  },
});
