# Changelog

All major changes to the LazyDog API project are documented here.  
We follow [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) and [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) principles.

---

## Release Tag Checklist (e.g. v0.2.0)
- [ ] All new features are merged into `main`
- [ ] Functionality is manually (or automatically) tested
- [ ] All relevant migrations are applied
- [ ] `CHANGELOG.md` is updated and accurate
- [ ] No debug code, `console.log`, `print()` or temporary mock remains
- [ ] Version number in README (if applicable) matches the tag
- [ ] Git tag is created: `git tag -a v0.2.0 -m "Release v0.2.0"`
- [ ] Tag is pushed: `git push origin v0.2.0`
- [ ] GitHub Release is created (optional but recommended)

---

## [Unreleased]

_This section lists unreleased changes._

<!-- 
Use this format when preparing the next version entry:

## [n.n.n] - YYYY-MM-DD

### Added
- Short clear statement about the new thing.

### Changed
- Short clear statement about what changed.

### Fixed
- Short clear statement about the bug fix.

### Removed
- Short clear statement about what's gone.
-->

_(Includes all changes up to and including 2025-05-05 — not yet released to production)_

## [0.2.0] - 2025-05-05
### Added
- feat(bookmark): implement secure and validated bookmark API (e3fd3f4)
- feat(resource): add ResourceItemViewSet with permissions and router-based URL routing (8a0b088)
- feat(rating): add RatingSerializer with validation and URL routing (ae205cb)
- feat(rating): add Rating model with score, user and resource_item relations (e7e86e0)
- feat: add ManyToMany relationship between ResourceItem and Tag (46891b9)
- feat: add tag support to ResourceItemSerializer (0fd7f40)
- feat: enable filtering and searching in ResourceItemViewSet (d73b982)
- feat: enforce admin-only tag management with custom permission (d978850)
- feature: add migration file for comment model (ecf04d2)
- feat: Create FlagSerializer with validation logic (5eccb00)
- feat: Register flag model in the Admin panel (b1b2aaf)
- feat(validation): add URL and description validation in ResourceItemSerializer (90e1c16)
- feat(admin): improve Category and ResourceItem admin views (f7ad467)
- feat: register comment model in admin site (464d965)
- feat: Add comment viewset to urls (36c1a75)
- feat: Add comment view and custom permission (4e3559f)
- feat: Add serializer for comment model (711cfe1)
- feat: Add comment model (2d0fbe2)
- feat: add comment app and url path (2b3b0c4)
- feat(category): add user association to Category model and serializer (5dd064e)
- feat: implement authentication and update URL paths (13754a6)
- feat(models): add category model and update resource item (15583e1)
- feat(category): add initial category app setup and routing (b5e576e)
- feat: Improve clarity of docstrings & comments in Tags (488136d)
- feat: add Tag model to database (0ca6d3d)
- feat: add tzdata for timezone support (62816f4)
- feat : add serializer to urls.py (5164711)
- feat : add urls (49a94e8)
- feat:add resource_item app and models (66ae554)
- Add rating app (0d224ef)
- Merge pull request #7 from ci-companeros/flag-dev (f556b65)
- Merge pull request #9 from ci-companeros/feature/resourceitem-tag (da144aa)
- config: enable filtering in REST API for better usability (c21fd5a)
- chore: add separate variable for debug and dev_db (3353c77)
- Add Flag app with initial model (df0fc8e)
- chore: Update dependencies in requirements.txt (f64a3ab)
- chore(gitignore): add Windsurf IDE and macOS system files to ignore list (fa93066)
- Update README.md (#2) (d17cba2)
- Chore: add bash alias files to gitignore file (e5cc524)
- chore : add models to admin.py (7e4619a)
- Revert "Remove env.py from tracking and add env.py.example template" (d535025)
- Revert "Improve security settings and add CORS configuration" (ce01c92)
- Improve security settings and add CORS configuration (2c0df5e)
- Merge pull request #1 from ci-companeros/jorgendev (bc94756)
- Add initial Django project structure with requirements and configuration files (b8ab6db)

### Changed
- refactor(api): improve views and serializers (2de49bf)
- refactor(rating): rename related_name on ForeignKey for clarity (6226312)
- refactor(settings): split DEBUG and DEV_DB for flexible environment control (6ad90ff)
- refactor: replace comment app with rating app in INSTALLED_APPS and clean whitespace (6c86a4c)
- refactor: update TagSerializer to restrict tag creation (41a7d93)
- refactor: Improve database selection logic in settings (749d8ff)
- refactor(settings, admin): clean up settings and resource admin (957110e)

### Fixed
- fix(settings): remove duplicate 'comment' app from INSTALLED_APPS (1a4fd4e)
- Fix: Validation in FlagSerializer to prevent duplicates (3384d48)
- fix: Correct typo in REST framework config key (2333bed)
- fix: correct tag endpoint to remove redundant path nesting (1234c80)
- fix(serializer): remove unused instance variable in validate_title (f63ee5c)
- fix(api): register ResourceItemViewSet in router to allow POST (4f91aa5)
- fix(settings): resolve merge conflict and add tag app (f0847ae)
- fix: Ensure Tag model integrity and code style (19a217b)
- Fix: Set secret key to correctly get key from env (8110429)

### Removed
- Remove env.py from tracking and add to .gitignore (8b8f068)
- Remove env.py from tracking and add env.py.example template (caf83fa)
- chore: remove test.py file (4cf01a1)

## [0.1.0] - 2025-03-01
### Added
- Initial commit (84ea004)
