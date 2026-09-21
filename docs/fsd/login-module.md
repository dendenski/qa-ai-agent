# Login Module - FSD

## FR-01 User Login
The user can log in with email and password.
- Email must be a valid format.
- Password must be 8-20 characters, with at least one uppercase letter and one number.

## FR-02 Account Lockout
After 5 consecutive failed attempts, the account is locked for 15 minutes.

## FR-03 Forgot Password
The user can request a reset link by email. The link expires after 30 minutes.