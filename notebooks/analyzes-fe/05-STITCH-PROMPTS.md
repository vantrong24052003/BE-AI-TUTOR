# Stitch UI Prompt - AI Tutor E-Learning Platform

## SINGLE COMPREHENSIVE PROMPT

```
Design a complete E-learning platform called "AI Tutor" with 16 screens. Premium, modern design with warm, approachable feel - NOT cold corporate or generic AI aesthetics.

═══════════════════════════════════════════════════════════════════════════════
COLOR PALETTE - Warm & Professional
═══════════════════════════════════════════════════════════════════════════════

Primary: #2563EB (Royal Blue) - trustworthy, educational
Secondary: #0891B2 (Teal) - fresh, modern
Accent: #F59E0B (Amber) - warm, encouraging, used for highlights & CTAs
Success: #059669 (Emerald) - achievements, completions
Error: #DC2626 (Red) - errors, warnings
Dark: #0F172A (Deep Navy) - text, headers
Light: #F8FAFC (Off-White) - backgrounds
Card: #FFFFFF (Pure White) - cards, elevated surfaces
Muted: #64748B (Slate Gray) - secondary text, placeholders
Border: #E2E8F0 (Light Gray) - subtle borders

Backgrounds: Clean white/light gray with subtle texture or very light geometric patterns
NO neon gradients, NO purple-pink-blue AI art style, NO dark mode as default

═══════════════════════════════════════════════════════════════════════════════
TYPOGRAPHY
═══════════════════════════════════════════════════════════════════════════════

Font: Inter or Plus Jakarta Sans
Headings: 600-700 weight, Deep Navy color
Body: 400-500 weight, Dark Slate color
Small: 400 weight, Muted Gray color

═══════════════════════════════════════════════════════════════════════════════
SCREEN 1: LANDING PAGE (/)
═══════════════════════════════════════════════════════════════════════════════

Layout: Single page scroll with sections

HEADER (sticky, white background, subtle shadow):
- Left: Logo "AI Tutor" with book + AI sparkle icon, Royal Blue
- Center: Navigation links (Features, Courses, Pricing) - clean hover underline
- Right: "Log in" text link, "Sign up" button (Royal Blue solid, rounded-full)

HERO SECTION:
- Background: Light cream (#FFFBF5) with subtle dot pattern
- Left column: Large heading "Learn Smarter, Not Harder" (Deep Navy), subheading "Personalized AI-powered learning that adapts to your pace", two CTAs: Primary "Get Started Free" (Amber, rounded-full), Secondary "Watch Demo" (outline)
- Right column: Illustration of student at laptop with friendly AI assistant character, soft shadows, modern flat illustration style
- Small trust badges below: "Trusted by 50,000+ learners" with avatar stack

FEATURES SECTION (white background):
- Section title "Why Choose AI Tutor?" centered
- 3 feature cards in row:
  * Card 1: Brain icon (Royal Blue), "AI-Powered Tutoring", "24/7 personalized help"
  * Card 2: Play icon (Teal), "Interactive Lessons", "Learn by doing, not just watching"
  * Card 3: Certificate icon (Amber), "Earn Certificates", "Industry-recognized credentials"
- Cards: White with soft shadow, rounded-xl (16px), hover lift effect

POPULAR COURSES SECTION (light gray background #F1F5F9):
- Section title "Popular Courses" with "View all →" link
- 4 course cards in grid (2 rows on desktop):
  * Card: White, rounded-xl, overflow hidden, shadow-sm
  * Top: Course thumbnail image (16:9), subtle gradient overlay at bottom
  * Content: Category pill (small, Royal Blue bg), Title (600 weight), Instructor name with avatar (small), Rating stars + count, Price (700 weight, Royal Blue or "Free" in Emerald)
  * Hover: Subtle scale (1.02), shadow increase

TESTIMONIALS SECTION (white background):
- Large quote card with left border accent (Amber)
- Student photo, name, course taken
- Star rating
- Carousel dots below

CTA SECTION (Royal Blue background):
- "Ready to Start Learning?" heading (white)
- "Join thousands of learners today" subtext
- "Create Free Account" button (Amber, rounded-full)

FOOTER (Deep Navy background):
- 4 columns: Brand + social icons, Learn links, Company links, Legal links
- Copyright at bottom
- All text in light colors

═══════════════════════════════════════════════════════════════════════════════
SCREEN 2: LOGIN PAGE (/auth/login)
═══════════════════════════════════════════════════════════════════════════════

Layout: Split screen 50/50

LEFT PANEL (Royal Blue background):
- Large "AI Tutor" logo (white)
- Abstract illustration of learning journey (dots connected by lines, books, graduation cap)
- "Welcome back!" text (white, large)
- "Continue your learning journey" subtext (light blue)

RIGHT PANEL (white):
- Centered form card (max-width 400px)
- "Log in" heading (Deep Navy)
- Email input (rounded-lg, border Gray, focus Royal Blue border)
- Password input with show/hide toggle
- "Remember me" checkbox + "Forgot password?" link (Royal Blue)
- "Log in" button (full width, Royal Blue, rounded-lg)
- Divider: "or continue with"
- Google button (outline, with Google icon)
- "Don't have an account? Sign up" link

═══════════════════════════════════════════════════════════════════════════════
SCREEN 3: REGISTER PAGE (/auth/register)
═══════════════════════════════════════════════════════════════════════════════

Same split layout as Login

LEFT PANEL: Same aesthetic, different illustration (person celebrating)
- "Join AI Tutor today!"

RIGHT PANEL:
- "Create account" heading
- Full name input
- Email input
- Password input with strength indicator (colored bar: red → yellow → green)
- Terms checkbox "I agree to Terms and Privacy Policy"
- "Create account" button (Royal Blue)
- Google signup option
- "Already have an account? Log in"

═══════════════════════════════════════════════════════════════════════════════
SCREEN 4: FORGOT PASSWORD (/auth/forgot-password)
═══════════════════════════════════════════════════════════════════════════════

Same split layout, smaller form

LEFT PANEL: Illustration of envelope with letter

RIGHT PANEL:
- "Reset your password" heading
- "Enter your email and we'll send you a reset link" subtext (Muted)
- Email input
- "Send reset link" button (Royal Blue)
- "← Back to login" link

SUCCESS STATE:
- Green checkmark icon (animated)
- "Check your email" heading
- "We sent a reset link to email@example.com"
- "Didn't receive it? Resend" link

═══════════════════════════════════════════════════════════════════════════════
SCREEN 5: APP SHELL - MAIN LAYOUT
═══════════════════════════════════════════════════════════════════════════════

SIDEBAR (fixed, 240px width, white background, right border):
- Top: Logo "AI Tutor" smaller version
- Navigation items (with icons, left aligned, 40px height each):
  * Dashboard (home icon) - active state: Royal Blue bg, white text
  * Courses (book icon)
  * My Learning (graduation cap icon)
  * AI Tutor (sparkle icon)
  * Profile (user icon)
- Bottom: Help & Support link, Logout button

TOP NAVBAR (sticky, white, subtle shadow):
- Left: Breadcrumb "Dashboard"
- Center: Search bar (rounded-full, gray background, search icon, placeholder "Search courses...")
- Right:
  * Notification bell icon with red dot badge
  * User avatar (circle, 36px) with dropdown arrow
  * Dropdown (on hover): Profile, Settings, Logout

MAIN CONTENT AREA:
- Background: Light gray (#F8FAFC)
- Padding: 24px
- Content varies by page

═══════════════════════════════════════════════════════════════════════════════
SCREEN 6: DASHBOARD (/app/dashboard)
═══════════════════════════════════════════════════════════════════════════════

WELCOME SECTION:
- "Good morning, Alex!" heading (time-based greeting)
- "You're making great progress. Keep it up!" subtext

STATS ROW (4 cards):
Card 1 - Courses in Progress:
- Book icon in Royal Blue circle
- "3" large number
- "Courses in progress" label

Card 2 - Lessons Completed:
- Check icon in Emerald circle
- "24" large number
- "Lessons completed" label

Card 3 - Hours Learned:
- Clock icon in Teal circle
- "12.5h" large number
- "Hours this week" label

Card 4 - Current Streak:
- Flame icon in Amber circle
- "7 days" large number
- "Learning streak 🔥" label

All cards: White, rounded-xl, shadow-sm, hover lift

CONTINUE LEARNING SECTION:
- Section title "Continue Learning"
- Horizontal scroll of 3 course cards:
  * Thumbnail (small, rounded-lg)
  * Course title
  * Progress bar (Royal Blue fill, gray track)
  * "Continue" button (outline, small)

RECOMMENDED COURSES:
- Section title "Recommended for You"
- Grid of 4 course cards (same style as landing page)

═══════════════════════════════════════════════════════════════════════════════
SCREEN 7: COURSE LIST (/app/courses)
═══════════════════════════════════════════════════════════════════════════════

PAGE HEADER:
- "All Courses" heading
- Breadcrumb: Home / Courses

FILTER BAR (sticky below navbar):
- Left: Category dropdown (All Categories, Programming, Design, Business...)
- Level dropdown (All Levels, Beginner, Intermediate, Advanced)
- Price dropdown (All, Free, Paid)
- Right: Sort dropdown (Most Popular, Newest, Highest Rated)
- Active filters shown as removable pills

SEARCH:
- Full-width search input with icon

COURSE GRID:
- 3 columns on desktop, 2 on tablet, 1 on mobile
- Course card (same as landing but larger):
  * Thumbnail (16:9 ratio)
  * Category pill (top left overlay)
  * Favorite heart icon (top right)
  * Title (truncates to 2 lines)
  * Instructor: avatar + name
  * Rating: stars + "(123)"
  * Students: user icon + "1.2k students"
  * Duration: clock icon + "10 hours"
  * Price: prominent, right aligned
  * Level badge: Beginner/Intermediate/Advanced

PAGINATION:
- Centered, numbered pages with prev/next arrows

═══════════════════════════════════════════════════════════════════════════════
SCREEN 8: COURSE DETAIL (/app/courses/:id)
═══════════════════════════════════════════════════════════════════════════════

HERO SECTION (gradient background based on category):
- Course title (large, white)
- Instructor info: avatar, name, "Instructor"
- Rating, students, duration, last updated
- Breadcrumb

TWO COLUMN LAYOUT:

LEFT COLUMN (2/3 width):

What you'll learn:
- Grid of 6 items with check icons

Course content:
- Accordion of modules:
  * Module header: "Module 1: Introduction" + lesson count + duration
  * Expanded: List of lessons with play icon, title, duration, preview badge
  * Completed lessons show checkmark

Description:
- Rich text with images

Reviews:
- Rating summary (average, star distribution bar)
- Individual review cards: avatar, name, rating, date, comment

RIGHT COLUMN (1/3 width, sticky):
- Course card:
  * Thumbnail
  * Price (large): "$49.99" or "Free"
  * Discount if applicable: crossed-out original price
  * "Enroll Now" button (Amber, full width, rounded-lg)
  * "Add to Wishlist" button (outline)
- Course includes list:
  * 10 hours of video
  * 5 articles
  * 20 downloadable resources
  * Certificate of completion
  * Full lifetime access

═══════════════════════════════════════════════════════════════════════════════
SCREEN 9: LEARNING PAGE (/app/learn/:courseId/lesson/:lessonId)
═══════════════════════════════════════════════════════════════════════════════

TWO COLUMN LAYOUT:

LEFT COLUMN (Video + Content):

VIDEO PLAYER:
- 16:9 aspect ratio, black background
- Custom controls (appear on hover):
  * Play/Pause (center large)
  * Progress bar with preview thumbnail
  * Volume slider
  * Settings (quality, speed)
  * Fullscreen
  * Picture-in-picture
- Lesson title below player

LESSON CONTENT:
- Description text
- Resources download links
- Notes section (expandable)

NAVIGATION:
- "Previous Lesson" "Mark Complete" "Next Lesson" buttons

RIGHT COLUMN (Course Sidebar, 320px):

COURSE INFO:
- Course title
- Progress: "45% complete" with progress bar

MODULE ACCORDION:
- Module 1 (expanded):
  * Lesson 1: Introduction ✓ (completed, green check)
  * Lesson 2: Getting Started ▶ (current, Royal Blue highlight)
  * Lesson 3: Basics 🔒 (locked, gray)
- Module 2 (collapsed):
  * 5 lessons • 45 min

═══════════════════════════════════════════════════════════════════════════════
SCREEN 10: QUIZ PAGE (/app/quiz/:quizId)
═══════════════════════════════════════════════════════════════════════════════

QUIZ HEADER:
- Quiz title
- Timer (circular progress): "14:30 remaining"
- Question indicator: "Question 3 of 10"

QUESTION CARD (centered, max-width 700px):
- Question text (large, bold)
- "Select one answer" or "Select all that apply"
- 4 option cards:
  * Letter badge (A, B, C, D)
  * Answer text
  * Hover: light blue background
  * Selected: Royal Blue border, checkmark

NAVIGATION:
- Progress dots (10 dots, answered = filled, current = ring)
- "Previous" "Next" "Submit Quiz" buttons

SIDEBAR (optional, collapsible):
- Question grid (clickable)
- Answered/unanswered count

═══════════════════════════════════════════════════════════════════════════════
SCREEN 11: QUIZ RESULT
═══════════════════════════════════════════════════════════════════════════════

PASS STATE:

CELEBRATION:
- Confetti animation
- Large trophy or medal icon (gold)
- "Congratulations!" heading (Emerald)
- "You passed the quiz!"

SCORE DISPLAY:
- Large circular progress: "85%" in center
- "You scored 85 out of 100"

STATS CARDS:
- Correct: 17 (green)
- Wrong: 3 (red)
- Time: 8:45

ACTIONS:
- "Review Answers" button (outline)
- "Retry Quiz" button (outline)
- "Continue Learning" button (Royal Blue, primary)

FAIL STATE:
- Encouraging icon (bookmark or retry arrow)
- "Keep practicing!" heading (Amber)
- "You need 70% to pass. You got 55%."
- Same stats display
- "Review Answers" and "Retry Quiz" prominent

═══════════════════════════════════════════════════════════════════════════════
SCREEN 12: AI TUTOR CHAT (/app/ai-tutor)
═══════════════════════════════════════════════════════════════════════════════

CHAT HEADER:
- "AI Tutor" title with sparkle icon
- Course context dropdown: "React Basics" (optional context)
- "New Chat" button (outline)

CHAT AREA (scrollable, light gray background):

AI MESSAGE (left-aligned):
- Avatar: AI icon in Royal Blue circle
- Message bubble: white, rounded-2xl, left-aligned tail
- Content: Markdown supported (code blocks, lists, bold)
- Timestamp: "2:30 PM"

USER MESSAGE (right-aligned):
- Avatar: User photo
- Message bubble: Royal Blue, rounded-2xl, right-aligned tail, white text
- Timestamp

TYPING INDICATOR:
- Three animated dots

QUICK SUGGESTIONS (below chat):
- Horizontal pills: "Explain this concept" "Give me an example" "Quiz me" "Summarize"

INPUT AREA (sticky bottom):
- Text input (auto-grow, rounded-2xl)
- Attachment icon (left)
- Send button (right, Royal Blue, appears when text entered)

═══════════════════════════════════════════════════════════════════════════════
SCREEN 13: MY COURSES (/app/my-courses)
═══════════════════════════════════════════════════════════════════════════════

PAGE HEADER:
- "My Learning" heading
- Stats: "3 in progress • 5 completed"

TABS:
- All | In Progress | Completed
- Active tab: Royal Blue underline

COURSE LIST:
Card style (horizontal):
- Left: Thumbnail (120x80px, rounded-lg)
- Middle:
  * Course title
  * Instructor name
  * Progress bar with percentage
  * "12 of 24 lessons completed"
- Right:
  * "Continue" button (primary) OR "View Certificate" (if completed)
  * Completed: Green checkmark badge

EMPTY STATE:
- Illustration of empty box
- "No courses yet"
- "Browse courses" button

═══════════════════════════════════════════════════════════════════════════════
SCREEN 14: PROFILE PAGE (/app/profile)
═══════════════════════════════════════════════════════════════════════════════

TWO COLUMN LAYOUT:

LEFT COLUMN (Sidebar navigation):
- Profile (active)
- Settings
- Certificates
- Help

RIGHT COLUMN:

PROFILE HEADER:
- Large avatar (120px) with "Change photo" button overlay
- Name (large)
- Email (muted)
- Member since date

STATS ROW:
- 3 stat cards: Courses enrolled, Hours learned, Certificates earned

ACHIEVEMENT BADGES:
- Section title "Achievements"
- Grid of badge icons (locked = gray, unlocked = colored)
  * "First Course" badge
  * "7-Day Streak" badge
  * "Quiz Master" badge
  * "Early Bird" badge

EDIT PROFILE FORM:
- Full name input
- Email input (readonly, with "Change email" link)
- Phone input
- Birthday input
- "Save Changes" button

═══════════════════════════════════════════════════════════════════════════════
SCREEN 15: SETTINGS PAGE (/app/profile/settings)
═══════════════════════════════════════════════════════════════════════════════

Same sidebar layout as Profile

TABS: Account | Notifications | Security | Appearance

ACCOUNT TAB:
- Language dropdown
- Timezone dropdown
- Delete account section (red text, danger zone)

NOTIFICATIONS TAB:
- Toggle switches with labels:
  * Email notifications (on)
  * Push notifications (off)
  * Learning reminders (on)
  * Course updates (on)
  * Promotional emails (off)

SECURITY TAB:
- Change password section:
  * Current password
  * New password
  * Confirm password
  * "Update password" button
- Active sessions:
  * "Chrome on Windows" - Current session (green dot) - "Active now"
  * "Safari on iPhone" - "Last active 2 days ago" - "Revoke" button

APPEARANCE TAB:
- Theme selection:
  * Light mode card (selected, Royal Blue border)
  * Dark mode card
  * System mode card

═══════════════════════════════════════════════════════════════════════════════
SCREEN 16: PAYMENT/CHECKOUT (/app/checkout/:courseId)
═══════════════════════════════════════════════════════════════════════════════

TWO COLUMN LAYOUT:

LEFT COLUMN (Order Summary):
- "Order Summary" heading
- Course card:
  * Thumbnail
  * Course title
  * Instructor
- Price breakdown:
  * Course price: $49.99
  * Discount: -$10.00 (green)
  * Total: $39.99 (large, bold)

RIGHT COLUMN (Payment):
- "Payment Method" heading
- Payment options (radio cards):
  * 💳 Credit/Debit Card (selected)
  * 🏦 Bank Transfer
  * 📱 E-wallet (Momo/ZaloPay)

CREDIT CARD FORM:
- Card number input with card type icon
- Expiry date / CVV row
- Cardholder name
- Save card checkbox

COUPON CODE:
- Input with "Apply" button
- Success: "Coupon applied! -$10.00"

SECURITY BADGES:
- 🔒 SSL secured
- Visa, Mastercard icons

ACTIONS:
- "Cancel" link
- "Pay $39.99" button (Amber, full width, large)

SUCCESS MODAL:
- Confetti animation
- Checkmark icon
- "Payment Successful!"
- "Start Learning Now" button

═══════════════════════════════════════════════════════════════════════════════
COMPONENT SPECIFICATIONS
═══════════════════════════════════════════════════════════════════════════════

BUTTONS:
- Primary: Royal Blue bg, white text, rounded-lg, hover: darker blue
- Secondary: Amber bg, Deep Navy text, rounded-lg
- Outline: White bg, Royal Blue border and text, rounded-lg
- Ghost: Transparent, Royal Blue text, hover: light blue bg
- Sizes: sm (32px h), md (40px h), lg (48px h)
- All buttons: 8px horizontal padding minimum, transition 150ms

INPUTS:
- Border: 1px Gray
- Border radius: lg (8px)
- Height: 40px default
- Focus: Royal Blue border 2px, subtle shadow
- Error: Red border, error message below
- Labels above input, 500 weight, small

CARDS:
- Background: White
- Border radius: xl (16px)
- Shadow: sm (subtle)
- Padding: 16-24px
- Hover: shadow md, slight lift

AVATARS:
- Circle
- Sizes: xs (24px), sm (32px), md (40px), lg (48px), xl (64px)
- Default: Initials on colored background

BADGES/PILLS:
- Rounded-full
- Small padding: 4px 8px
- Font size: xs (12px)
- Colors match context

PROGRESS BARS:
- Height: 8px
- Track: Light Gray
- Fill: Royal Blue
- Border radius: full (rounded)
- Animated fill on load

TOAST NOTIFICATIONS:
- Top-right position
- Icons: success (green check), error (red x), warning (amber !), info (blue i)
- Auto-dismiss after 5 seconds
- Slide-in animation

MODALS:
- Centered
- Backdrop: semi-transparent black
- Card: white, rounded-xl, shadow-xl
- Close button (x) top right
- Slide-up animation

═══════════════════════════════════════════════════════════════════════════════
INTERACTIONS & ANIMATIONS
═══════════════════════════════════════════════════════════════════════════════

- Hover states: 150ms ease transition
- Button press: scale(0.98)
- Page transitions: fade 200ms
- Loading: skeleton screens with shimmer
- Success actions: subtle checkmark pop animation
- Card hover: translateY(-2px), shadow increase
- Dropdown: slide down 150ms
- Modal: fade in + slide up 200ms
- Toast: slide in from right 200ms

═══════════════════════════════════════════════════════════════════════════════
RESPONSIVE BREAKPOINTS
═══════════════════════════════════════════════════════════════════════════════

Mobile (<640px):
- Sidebar: Hidden, hamburger menu
- Bottom navigation bar (Dashboard, Courses, AI Tutor, Profile)
- Cards: Full width
- Forms: Full width

Tablet (640px-1024px):
- Sidebar: Collapsed (icons only, 64px)
- Hover to expand
- Cards: 2 columns

Desktop (>1024px):
- Full sidebar (240px)
- Cards: 3-4 columns

═══════════════════════════════════════════════════════════════════════════════

Design with attention to detail. Every element should feel intentional and polished. Use consistent spacing (8px grid system). Prioritize readability and usability. Make it feel like a premium product worth paying for.
```

---

*Version: 3.0 - Single Comprehensive Prompt*
