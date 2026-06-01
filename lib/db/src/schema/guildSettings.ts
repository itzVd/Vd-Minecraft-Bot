import { pgTable, text, integer, timestamp } from "drizzle-orm/pg-core";
import { createInsertSchema } from "drizzle-zod";
import { z } from "zod/v4";

export const guildSettingsTable = pgTable("guild_settings", {
  guildId:          text("guild_id").primaryKey(),
  minecraftIp:      text("minecraft_ip"),
  minecraftPort:    integer("minecraft_port").default(25565),
  minecraftType:    text("minecraft_type").default("java"),
  welcomeChannelId: text("welcome_channel_id"),
  updatedAt:        timestamp("updated_at").defaultNow(),
});

export const insertGuildSettingsSchema = createInsertSchema(guildSettingsTable).omit({ updatedAt: true });
export type InsertGuildSettings = z.infer<typeof insertGuildSettingsSchema>;
export type GuildSettings = typeof guildSettingsTable.$inferSelect;
