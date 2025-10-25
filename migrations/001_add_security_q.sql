-- Migration: add security question columns to account tables
-- Run this against the prometricdb database.

ALTER TABLE student
  ADD COLUMN security_question VARCHAR(255) NULL,
  ADD COLUMN security_answer VARCHAR(255) NULL;

ALTER TABLE employee_personal
  ADD COLUMN security_question VARCHAR(255) NULL,
  ADD COLUMN security_answer VARCHAR(255) NULL;

ALTER TABLE managers
  ADD COLUMN security_question VARCHAR(255) NULL,
  ADD COLUMN security_answer VARCHAR(255) NULL;

-- After running, you may prompt existing users to set their security Q/A on next login.
