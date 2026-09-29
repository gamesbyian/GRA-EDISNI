# One-shot Discord archive

This repository includes a deliberately narrow, one-shot Discord history exporter for use when a server administrator has explicitly authorized archival access.

The exporter uses a normal Discord bot account and Discord's HTTPS API. It does **not** automate a user account.

## What the administrator needs to do

The server administrator does not need to host anything or share credentials.

They only need to authorize the bot into the server and grant it access to the channels/categories they are comfortable exporting.

Minimum channel permissions:

- View Channel
- Read Message History

Do not grant Administrator, Manage Messages, Send Messages, Manage Channels, or Manage Roles for this archival job.

The bot should only be able to see the channels that are in scope for the archive.

## One-time setup by the bot owner

1. Open the Discord Developer Portal.
2. Create a new application, for example `INSIDE Archive`.
3. Add a bot user to the application.
4. On the bot settings page, enable **Message Content Intent**. For an unverified one-server bot this can be enabled directly in the Developer Portal.
5. Copy/reset the bot token.
6. In this GitHub repository, create an Actions secret named `DISCORD_BOT_TOKEN` containing that token.
7. From the application's installation/OAuth settings, generate a server-install link for the bot. Request only:
   - View Channel
   - Read Message History
8. Send the install link plus the admin-request text to a server administrator.

Never commit the bot token, paste it into an issue/PR/chat, or send it to the server administrator.

## Running the export

Once the bot is in the server:

1. In Discord, enable Developer Mode if necessary and copy the server ID.
2. Open GitHub Actions -> **One-shot Discord archive** -> **Run workflow**.
3. Enter the server ID.
4. The workflow defaults to the exact channel name `stickers-solving` for the first INSIDE archive. Change or clear that field as needed; exact channel/thread IDs can also be supplied.
5. If both channel names and IDs are blank, the script attempts every text-capable channel visible to the bot.
6. Choose whether to include archived public threads and download attachments.
7. Run the workflow.
8. Download the resulting `discord-export-<guild-id>` Actions artifact.

The artifact is retained for seven days by default. The workflow does not commit Discord content to Git.

## Export shape

```
discord-export/
  manifest.json
  channels/
    <channel-name>--<channel-id>.json
  attachments/
    <channel-id>/
      <message-id>/
        <attachment-id>--<filename>
```

Each channel JSON file preserves the Discord message objects returned by the API, including message IDs, timestamps, authors, replies/references, embeds, reactions and attachment metadata when Discord supplies them.

`manifest.json` records the guild identity, channel IDs/names and exported message counts. The bot token is never written to output.

## Scope and limitations

- The script reads only channels the bot can access.
- It does not post, react, edit, delete, enumerate members, or alter server state.
- Active threads are included when visible.
- Archived **public** threads can be enumerated with the workflow option.
- Archived private-thread discovery is intentionally omitted from this minimal exporter.
- Attachment CDN links can expire, so select attachment downloading if the files themselves are important.
- Very large servers may exceed the workflow timeout or artifact size limits. For this project, prefer restricting access to the relevant research categories/channels if the server is large.
- After the archive is verified, the administrator can remove the bot and the repository owner can delete/rotate the token.

## After export

Treat the raw archive as source evidence, not as a semantic conclusion. Before committing any derived research data to this repository:

- preserve message/channel IDs and timestamps for provenance;
- distinguish Discord claims from independently verified observations;
- avoid importing unrelated personal conversation;
- keep large binary attachments out of ordinary Git history unless they are genuinely needed as durable evidence.
