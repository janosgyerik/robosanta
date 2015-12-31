RoboSanta
=========

I'm a [bot on Code Review][cr-user]. I periodically post links to selected questions/answers in the [The 2nd Monitor][the-2nd-monitor].

Topics:

- [Naruto answers][naruto]: accepted non-selfie answer with 0 score per day

- [Ripe zombies][ripe-zombie]: open question with answers, at least one answer having score 0, no answer having score > 0

- (coming soon) [Code-only answers][code-only-answers]: answers that contain only a code block, without explanation

- (coming soon) [Bad Naruto answers][bad-naruto]: selfie accepted answers with zero or negative score

I post one random entry from each topic at 9:00 UTC and 21:00 UTC.

Feature requests
----------------

See [GitHub issues][issues] for pending features. It's also the place to register new feature requests.

Before asking for a new feature, please ask the community first in the [The 2nd Monitor][the-2nd-monitor] chat room.

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

[the-2nd-monitor]: http://chat.stackexchange.com/rooms/8595/the-2nd-monitor
[issues]: https://github.com/janosgyerik/robosanta/issues
[cr-user]: http://codereview.stackexchange.com/users/75639/robosanta
[naruto]: http://meta.codereview.stackexchange.com/a/4946/12390
[ripe-zombie]: http://meta.codereview.stackexchange.com/a/4970/12390
[code-only-answers]: http://meta.codereview.stackexchange.com/a/5659/12390
[bad-naruto]: http://meta.codereview.stackexchange.com/a/5660/12390
