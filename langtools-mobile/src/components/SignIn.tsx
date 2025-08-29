import { useSignIn, useSignUp } from '@clerk/clerk-expo'
import { EmailCodeFactor, SignInFirstFactor } from '@clerk/types'
import { useRouter } from 'expo-router'
import React, { useCallback, useMemo } from 'react'
import { Text, TextInput, TouchableOpacity, View } from 'react-native'
import { clerkErrorEmailExistsSchema } from '../utils/clerkError'

export function SignIn() {
  const signUp = useSignUp()
  const signIn = useSignIn()
  const router = useRouter()
  const [emailExists, setEmailExists] = React.useState('')

  const [emailAddress, setEmailAddress] = React.useState('')
  const [otpSent, setOtpSent] = React.useState(false)
  const [otp, setOtp] = React.useState('')

  const isLoaded = useMemo(() => {
    return signUp.isLoaded || signIn.isLoaded
  }, [signUp, signIn])

  const onSendEmailSignIn = useCallback(async () => {
    if (!isLoaded || !signIn.signIn) return

    try {
      const { supportedFirstFactors } = await signIn.signIn.create({
        identifier: emailAddress,
        strategy: 'email_code',
      })

      const isEmailCodeFactor = (
        factor: SignInFirstFactor,
      ): factor is EmailCodeFactor => {
        return factor.strategy === 'email_code'
      }

      const emailCodeFactor = supportedFirstFactors?.find(isEmailCodeFactor)

      if (!emailCodeFactor) {
        throw new Error('No email code factor found')
      }

      await signIn.signIn.prepareFirstFactor({
        strategy: 'email_code',
        emailAddressId: emailCodeFactor.emailAddressId,
      })

      setOtpSent(true)
    } catch (err) {
      console.error(JSON.stringify(err, null, 2))
    }
  }, [emailAddress, isLoaded, signIn.signIn])

  // Handle the submission of the sign-in form
  const onSendEmailSignUp = useCallback(async () => {
    if (!isLoaded || !signUp.signUp) return

    // Start the sign-in process using the email and password provided
    try {
      await signUp.signUp.create({
        emailAddress: emailAddress,
      })

      await signUp.signUp.prepareEmailAddressVerification()
      setOtpSent(true)
    } catch (err) {
      const errorParsed = clerkErrorEmailExistsSchema.safeParse(err)
      if (errorParsed.success) {
        setEmailExists(emailAddress)
        onSendEmailSignIn()
        return
      }
      // See https://clerk.com/docs/custom-flows/error-handling
      // for more info on error handling
      console.error(JSON.stringify(err, null, 2))
    }
  }, [emailAddress, isLoaded, onSendEmailSignIn, signUp.signUp])

  const onVerifyOtpSignUp = useCallback(async () => {
    if (!signUp.signUp) {
      console.error('signUp.signUp is not loaded')
      return
    }
    const signUpAttempt = await signUp.signUp.attemptEmailAddressVerification({
      code: otp,
    })

    // If sign-in process is complete, set the created session as active
    // and redirect the user
    if (signUpAttempt.status === 'complete') {
      await signUp.setActive({ session: signUpAttempt.createdSessionId })
    } else {
      // If the status isn't complete, check why. User might need to
      // complete further steps.
      console.error(JSON.stringify(signUpAttempt, null, 2))
    }
  }, [otp, signUp])

  const onVerifyOtpSignIn = useCallback(async () => {
    if (!signIn.signIn) {
      console.error('signIn.signIn is not loaded')
      return
    }

    const signInAttempt = await signIn.signIn.attemptFirstFactor({
      strategy: 'email_code',
      code: otp,
    })

    if (signInAttempt.status === 'complete') {
      await signIn.setActive({ session: signInAttempt.createdSessionId })
    } else {
      console.error(JSON.stringify(signInAttempt, null, 2))
    }
  }, [otp, signIn])

  const onVerifyOtp = useCallback(async () => {
    if (emailExists === emailAddress) {
      await onVerifyOtpSignIn()
    } else {
      await onVerifyOtpSignUp()
    }
    router.replace('/')
  }, [emailExists, emailAddress, router, onVerifyOtpSignUp, onVerifyOtpSignIn])

  return (
    <View>
      <Text>Sign in</Text>
      <TextInput
        autoCapitalize="none"
        value={emailAddress}
        placeholder="Enter email"
        onChangeText={(emailAddress) => setEmailAddress(emailAddress)}
        editable={!otpSent}
        inputMode="email"
        textContentType="emailAddress"
      />
      {otpSent && (
        <TextInput
          autoCapitalize="none"
          value={otp}
          placeholder="Enter OTP"
          onChangeText={(otp) => setOtp(otp)}
        />
      )}
      {!otpSent && (
        <TouchableOpacity onPress={onSendEmailSignUp}>
          <Text>Send email</Text>
        </TouchableOpacity>
      )}
      {otpSent && (
        <TouchableOpacity onPress={onVerifyOtp}>
          <Text>Verify OTP</Text>
        </TouchableOpacity>
      )}
    </View>
  )
}
