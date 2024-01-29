import { MetadataRoute } from "next";

export default function sitemap(): MetadataRoute.Sitemap {
  return [
    {
      url: "https://TalentSpire.blufitech.com",
      lastModified: new Date(),
    },
    {
      url: "https://TalentSpire.blufitech.com/demo",
      lastModified: new Date(),
    },
  ];
}
