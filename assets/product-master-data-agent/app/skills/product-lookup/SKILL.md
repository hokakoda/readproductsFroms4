---
name: product-lookup
description: Instructions for querying product master data from SAP S/4HANA — covers lookup by product ID, name, and category, partial match handling, and no-result communication.
---

# Product Master Data Lookup

## When to Use This Skill

Load this skill when a Sales Representative asks about a product — its description, specifications, category, or any other master data attributes stored in SAP S/4HANA.

## Instructions

### Step 1: Identify the Query Type

Determine how the user is searching for the product:

| User Input | Query Type |
|------------|-----------|
| Provides an exact product ID (e.g., "P-1001", "MX-1234") | Lookup by exact product ID |
| Provides a product name or partial name (e.g., "pump", "industrial filter") | Search by name |
| Provides a category (e.g., "Pumps", "Electronics") | Search by category |
| Query is ambiguous | Ask a clarifying question before calling any tool |

### Step 2: Execute the Query

#### Lookup by Exact Product ID
- Call the product master tool with the exact `Product` key field value provided by the user.
- Return the product's description and key specification fields.

#### Search by Name (Partial Match)
- Call the product master tool using a `$filter` on the product description field with the user's search term.
- Set `$top` to a maximum of 100 results.
- If multiple results are returned, present a concise list (product ID + description) and ask the user to select one before providing full details.

#### Search by Category
- Call the product master tool using a `$filter` on `ProductGroup` or `ProductType` with the user's specified category.
- Set `$top` to a maximum of 100 results.
- Present results as a list with product ID and description.

### Step 3: Format and Return the Result

Return product information in a clear, concise format:

```
Product ID: [ID]
Description: [Full description]
Product Type: [Type]
Product Group: [Group/Category]
Base Unit of Measure: [Unit]
[Additional specifications if available]
```

If multiple products match, list them briefly and ask the user to confirm which one they want full details for.

### Step 4: Handle Edge Cases

#### No Results Found
If the tool returns an empty result set:
1. Inform the user clearly: "No product found matching '[search term]'."
2. Suggest refinements: "Try searching with a shorter term, a different category, or the exact product ID."
3. Do NOT fabricate or guess a product.

#### Tool Error
If the tool returns an error:
1. Report the error message exactly as received.
2. Inform the user: "The product data system is currently unavailable. Please try again shortly."
3. Do NOT attempt to provide cached or estimated data.

#### Ambiguous Query
If the query could match multiple search types (e.g., "P100" could be an ID or partial name):
1. Ask the user: "Are you looking for a product with ID 'P100', or searching for products with 'P100' in their name?"
2. Wait for the user's confirmation before calling any tool.
