---
name: Shopify Developer
description: Liquid templates, APIs, app development, and theme customization
---

# Shopify Developer Skill

## Liquid Basics

```liquid
{% comment %} Variables {% endcomment %}
{{ product.title }}
{{ product.price | money }}

{% comment %} Loops {% endcomment %}
{% for product in collection.products %}
  <h2>{{ product.title }}</h2>
{% endfor %}

{% comment %} Conditionals {% endcomment %}
{% if product.available %}
  <button>Add to Cart</button>
{% else %}
  <span>Sold Out</span>
{% endif %}

{% comment %} Filters {% endcomment %}
{{ 'hello' | capitalize }}  {# Hello #}
{{ product.price | money }}  {# $19.99 #}
{{ 'now' | date: '%Y-%m-%d' }}
```

## Theme Structure

```
theme/
├── assets/          # CSS, JS, images
├── config/          # settings_schema.json
├── layout/          # theme.liquid
├── locales/         # translations
├── sections/        # reusable blocks
├── snippets/        # partials
└── templates/       # page templates
```

## Common Objects

| Object | Use |
|--------|-----|
| `product` | Current product data |
| `collection` | Collection of products |
| `cart` | Shopping cart |
| `customer` | Logged-in customer |
| `shop` | Store settings |
| `settings` | Theme settings |

## Storefront API (GraphQL)

```graphql
query {
  products(first: 10) {
    edges {
      node {
        id
        title
        priceRange {
          minVariantPrice {
            amount
          }
        }
      }
    }
  }
}
```

## Admin API

```javascript
const Shopify = require('shopify-api-node');

const shopify = new Shopify({
  shopName: 'your-store',
  accessToken: 'shpat_xxx'
});

const products = await shopify.product.list({ limit: 50 });
```

## Metafields

```liquid
{{ product.metafields.custom.sizing_guide }}
```

## When to Apply
Use when building Shopify themes, apps, or customizing stores.
