RoboSanta
=========

I'm a bot. This is what I do:

- Post a random Naruto answer (accepted with 0 score) in [The 2nd Monitor][1] chat room, at 21:00 UTC.

- TODO: Post recent answers in [The 2nd Monitor][1] chat room, for users eligible for [Epic][2] or [Legendary][3], when they are close to rep-cap, at 11pm.

*(For the record: I don't actually give out any upvotes, like a "real Santa" would. But I hope to inspire ;-)*

Feature requests
----------------

See [GitHub issues][4] for pending features. It's also the place to register new feature requests.

Before asking for a new feature, please ask the community first in the [The 2nd Monitor][1] chat room!

### Completed and released

- *Don't post Naruto answers to questions that were closed as off-topic* by [@Vogel](http://codereview.stackexchange.com/users/37660/vogel612)

### Won't do

- *You currently look for answers with 0 score. I think 0 votes would be more relevant, to prevent answers with equal + and - votes from popping up.* by [SirPython](http://codereview.stackexchange.com/users/59481/sirpython)
  + Won't do. Currently I'm using the official Stack Exchange API to get information about posts.
    The API exposes only the *score*, not the up-down-vote count details. To get the votes counts,
    I would need two things: use web scraping instead of the API (shaky solution);
    beef up [@RoboSanta](http://codereview.stackexchange.com/users/75639/robosanta) with enough rep
    so that he can see the up-down-vote counts.
- *RoboSanta should not post accepted answers with any votes at all.  Only answers with zero votes.* by anon
  + Same issue as the previous.

  [1]: http://chat.stackexchange.com/rooms/8595/the-2nd-monitor
  [2]: http://codereview.stackexchange.com/help/badges/26/epic
  [3]: http://codereview.stackexchange.com/help/badges/27/legendary
  [4]: https://github.com/janosgyerik/robosanta/issues
