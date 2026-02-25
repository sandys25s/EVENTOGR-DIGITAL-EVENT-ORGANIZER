# Digital Event Organizer Sample Test Cases

| TC ID | Test Scenario | Steps to Perform | Expected Result |
|-------|---------------|------------------|-----------------|
| TC_01 | User Registration | 1. Navigate to Register page<br>2. Enter valid details<br>3. Submit | Account created; Redirected to Login page. |
| TC_02 | Admin Login | 1. Enter admin credentials<br>2. Submit | Successful login; Redirected to Admin Dashboard. |
| TC_03 | Event Creation | 1. Go to "Create Event"<br>2. Fill all fields<br>3. Click Publish | Event appears on Home and Events page. |
| TC_04 | Free Registration | 1. Login as User<br>2. Select a free event<br>3. Click Register | Registration successful; Notification received. |
| TC_05 | Paid Registration | 1. Select a paid event<br>2. Click Pay & Register<br>3. Enter mock card details<br>4. Submit | Payment success; Registration confirmed. |
| TC_06 | Limit Enforcement | 1. Fill an event to max participants<br>2. Try to register as another user | System shows "Event is full" or disables button. |
| TC_07 | Admin CRUD | 1. Edit an existing event title<br>2. Delete an event | Changes reflect immediately in the database and UI. |
| TC_08 | Unauthorized Access | 1. Try to access `/admin/dashboard` without login | Redirected to Login page. |
| TC_09 | Invalid Login | 1. Enter wrong password for existing email | Error message: "Invalid email or password". |
| TC_10 | Notification View | 1. Perform registration<br>2. Check Dashboard | Notification message appears in the sidebar. |
