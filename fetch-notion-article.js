const { Client } = require('@notionhq/client');

// Initialize a new Notion client
const notion = new Client({ auth: process.env.NOTION_API_KEY });

// Fetch the latest article data from Notion
async function fetchLatestArticle() {
  const databaseId = process.env.NOTION_DATABASE_ID;

  // Fetch the database and its properties
  const { properties } = await notion.databases.retrieve({
    database_id: databaseId,
  });

  // Get the ID of the "published" status
  const statusId = Object.keys(properties).find(
    (id) => properties[id].title && properties[id].title[0].text.content === 'Status'
  );

  // Filter pages by the "published" status
  const { results } = await notion.databases.query({
    database_id: databaseId,
    filter: {
      property: statusId,
      select: {
        equals: 'published',
      },
    },
    sorts: [
      {
        property: 'Published',
        direction: 'descending',
      },
    ],
    page_size: 1,
  });

  // Get the latest article
  const latestArticle = results[0];

  // Return the title and content of the latest article
  return {
    title: latestArticle.properties.Title.title[0].text.content,
    content: latestArticle.properties.Content.rich_text[0].text.content,
  };
}

// Call the fetchLatestArticle function and output the results
fetchLatestArticle().then((article) => {
  console.log(`NOTION_ARTICLE_TITLE=${article.title}`);
  console.log(`NOTION_ARTICLE_CONTENT=${article.content}`);
});
