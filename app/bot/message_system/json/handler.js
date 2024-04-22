data = {
  content: "@Everyone",
  Embeds: [
    {
      content: "This Embed",
      color: "0xffffff",
      description: "this data for new data",
      attachments: {
        set_author: {
          content: "Hello im Author!",
          name: "Dan",
          url: "http://localhost:5345",
          icon_url: "http://localhost:5345",
        },
        set_footer: {
          content: "Im Footer",
          icon_url: "http://localhost/url/img",
        },
        set_image: {
          url: "http://localhost/url/img",
        },
        set_thumbnail: {
          url: "http://localhost/url/img",
        },
        add_field: {
          content: "Im new fIELD",
          name: "mY nAME",
          value: null,
          inline: true,
        },
        set_field_at: {
          index: 1,
          name: "hee",
          value: null,
          inline: false,
        },
      },
    },
    {
      content: "This Embed",
      color: "0xffffff",
      description: "this data for new data",
      attachments: {
        set_author: {
          content: "Hello im Author!",
          name: "Dan",
          url: "http://localhost:5345",
          icon_url: "http://localhost:5345",
        },
        set_footer: {
          content: "Im Footer",
          icon_url: "http://localhost/url/img",
        },
        set_image: {
          url: "http://localhost/url/img",
        },
        set_thumbnail: {
          url: "http://localhost/url/img",
        },
        add_field: {
          content: "Im new fIELD",
          name: "mY nAME",
          value: null,
          inline: true,
        },
        set_field_at: {
          index: 1,
          name: "hee",
          value: null,
          inline: false,
        },
      },
    },
  ],
};

async function handlerDataJsonToEmbedMessageDiscord(data) {
  if (!data.content) {
    return console.error("Отсутсвует поле <<'content'>> ");
  }
  if (!data.Embeds) {
    return console.error("Отсутсвует поле <<'Embeds'>> ");
  }
  if (data.Embeds.length > 10) {
    return console.error("Максимальное количество Embeds - 10");
  }
  for (let i = 0; i < data.Embeds.length; i++) {
    if (!data.Embeds[i].content) {
      return console.error("Отсутсвует поле <<'content'>> в Embeds");
    } else if (!data.Embeds[i].color) {
      return console.error("Отсутсвует поле <<'color'>> в Embeds");
    } else if (!data.Embeds[i].description) {
      return console.error("Отсутсвует поле <<'description'>> в Embeds");
    } else {
      if (!data.Embeds[i].attachments) {
        console.error("Отсутсвует поле <<'attachments'>> в Embeds");
      } else {
        for (let key in data.Embeds[i].attachments) {
          if (key === "add_field") {
            if (!data.Embeds[i].attachments[key].content) {
              return console.error(
                "Отсутсвует поле <<'content'>> в Embeds.attachments.add_field"
              );
            } else if (!data.Embeds[i].attachments[key].name) {
              return console.error(
                "Отсутсвует поле <<'name'>> в Embeds.attachments.add_field"
              );
            }
          }
          if (key === "set_field_at") {
            if (!data.Embeds[i].attachments[key].index) {
              return console.error(
                "Отсутсвует поле <<'index'>> в Embeds.attachments.set_field_at"
              );
            }
          }
          if (key === "set_author") {
            if (!data.Embeds[i].attachments[key].content) {
              return console.error(
                "Отсутсвует поле <<'content'>> в Embeds.attachments.set_author"
              );
            } else if (!data.Embeds[i].attachments[key].name) {
              return console.error(
                "Отсутсвует поле <<'name'>> в Embeds.attachments.set_author"
              );
            } else if (!data.Embeds[i].attachments[key].url) {
              return console.error(
                "Отсутсвует поле <<'url'>> в Embeds.attachments.set_author"
              );
            } else if (!data.Embeds[i].attachments[key].icon_url) {
              return console.error(
                "Отсутсвует поле <<'icon_url'>> в Embeds.attachments.set_author"
              );
            }
          }
          if (key === "set_footer") {
            if (!data.Embeds[i].attachments[key].content) {
              return console.error(
                "Отсутсвует поле <<'content'>> в Embeds.attachments.set_footer"
              );
            } else if (!data.Embeds[i].attachments[key].icon_url) {
              return console.error(
                "Отсутсвует поле <<'icon_url'>> в Embeds.attachments.set_footer"
              );
            }
          }
          if (key === "set_image") {
            if (!data.Embeds[i].attachments[key].url) {
              return console.error(
                "Отсутсвует поле <<'url'>> в Embeds.attachments.set_image"
              );
            }
          }
          if (key === "set_thumbnail") {
            if (!data.Embeds[i].attachments[key].url) {
              return console.error(
                "Отсутсвует поле <<'url'>> в Embeds.attachments.set_thumbnail"
              );
            }
          }
        }
      }
    }
    return console.log(data);
  }
}

handlerDataJsonToEmbedMessageDiscord(data);
