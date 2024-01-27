import { pgTable, serial, text, varchar } from "drizzle-orm/pg-core";

export const transcripts = pgTable("transcripts", {
	id: serial("id").primaryKey(),
	filename: varchar("filename"),
	transcript: text("transcript"),
});

