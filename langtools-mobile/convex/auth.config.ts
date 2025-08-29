console.log(
  'process.env.CLERK_JWT_ISSUER_DOMAIN',
  process.env.CLERK_JWT_ISSUER_DOMAIN,
)

export default {
  providers: [
    {
      domain: 'https://magical-mammal-70.clerk.accounts.dev',
      applicationID: 'convex',
    },
  ],
}
