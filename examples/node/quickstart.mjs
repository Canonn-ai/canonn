// Ask Canonn R1 a question about your own document.
//   npm install openai
//   CANONN_API_KEY=... node quickstart.mjs
import OpenAI from 'openai';

const client = new OpenAI({ baseURL: 'https://api.canonn.ai/v1', apiKey: process.env.CANONN_API_KEY });

const document = 'Northwind returns policy.\nReturns are accepted within 30 days of delivery.';

const reply = await client.chat.completions.create({
  model: 'canonn-r1',
  messages: [
    { role: 'system', content: `Answer from this document.\n\n${document}` },
    { role: 'user', content: 'Can I return an order after six weeks?' },
  ],
});
console.log(reply.choices[0].message.content);
