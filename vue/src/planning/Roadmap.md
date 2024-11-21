# Roadmap

## LenseQuery

### POC initial setup

- [ ] Done

#### Test cases

- **Data:** Retrieve `user` and `userSettings`
- **UI:** See current user settings on the page
- **Data:** Update `user` and `userSettings`
  - Make sure that it updates live on other clients

#### Ideas

- Test multiple tabs
- Test multiple browsers
- Test concurrent access from different devices and network endpoints

#### LenseQuery design

[./LenseQuery.ts](./LenseQuery.ts)

- `LenseQuery.fetchMainDb` types are made with json-schema and are shared across TS and Go environments
- [ ] Provide unified API for all models

#### Setup

- Playwright test runner
- Can run agains live database
- Creates mock user data, that exists like live data, but marked so that it could be
  excluded from statistics or cleaned up effectively
- Ability to be authotized by an arbitrary TEST user
- Automatic authorization will return data of the test user
