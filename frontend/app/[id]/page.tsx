import { neon } from "@neondatabase/serverless";
import { drizzle } from "drizzle-orm/neon-http";
import { eq } from "drizzle-orm";

import { transcripts } from "@/lib/schema";
import { db } from "@/lib/db";

async function getTranscript({ id }: { id: number }) {
	const result = await db
		.select({ transcript: transcripts.transcript })
		.from(transcripts)
		.where(eq(transcripts.id, id));

	return result[0].transcript;
}

export default async function Page({ params }: { params: { id: string } }) {
	const transcript = await getTranscript({ id: parseInt(params.id) });

	return (
		<div className="min-h-screen text-gray-900 antialiased mx-auto max-w-[800px]">
			{transcript}
		</div>
	);
}
