async def sync_callback(response, bot):
    bot.logger.log(
        f"Sync response received (next batch: {response.next_batch})", "debug"
    )

    bot.sync_response = response

    await bot.accept_pending_invites()
