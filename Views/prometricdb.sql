-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Oct 21, 2025 at 02:02 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `prometricdb`
--

-- --------------------------------------------------------

--
-- Table structure for table `employee_personal`
--

CREATE TABLE `employee_personal` (
  `employee_id` int(10) NOT NULL,
  `email_id` varchar(50) NOT NULL,
  `Name` varchar(30) NOT NULL,
  `tutored_subject` varchar(20) NOT NULL,
  `center` varchar(20) NOT NULL,
  `date_joined` date NOT NULL,
  `password` varchar(30) NOT NULL,
  `role` varchar(100) NOT NULL,
  `security_question` varchar(255) DEFAULT NULL,
  `security_answer` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `employee_personal`
--

INSERT INTO `employee_personal` (`employee_id`, `email_id`, `Name`, `tutored_subject`, `center`, `date_joined`, `password`, `role`, `security_question`, `security_answer`) VALUES
(1, 'neilbarot5@gmail.com', 'Neil Barot', 'Python', 'ahmedabad', '2025-06-20', 'neil1234', 'Tutor', NULL, NULL),
(8, 'devamin1@gmail.com', 'Dev Amin', 'Maths', 'ahmedabad', '2025-07-03', 'dev1234', 'Tutor', NULL, NULL),
(9, 'hetpatel1@gmail.com', 'Het Patel', 'Java', 'Ahmedabad', '2025-07-03', 'het1234', 'Tutor', NULL, NULL),
(10, 'akshatshah1@gmail.com', 'Akshat shah', 'Biology', 'ahmedabad', '2025-07-03', 'akshat1234', 'Tutor', NULL, NULL),
(11, 'vedpatel1@gmail.com', 'Ved patel', 'Chemistry', 'ahmedabad', '2025-07-03', 'ved1234', 'Tutor', NULL, NULL),
(13, 'riapatel1@gmail.com', 'Ria Patel', 'Physics', 'AHmedabad', '2025-07-10', 'ria1234', 'Tutor', NULL, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `improvements`
--

CREATE TABLE `improvements` (
  `id` int(11) NOT NULL,
  `name` varchar(100) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `message` text DEFAULT NULL,
  `submitted_on` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `kpi_categories`
--

CREATE TABLE `kpi_categories` (
  `id` int(10) NOT NULL,
  `name` varchar(20) NOT NULL,
  `weight_percent` float NOT NULL,
  `description` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `managers`
--

CREATE TABLE `managers` (
  `id` int(50) NOT NULL,
  `email_id` varchar(50) NOT NULL,
  `name` varchar(50) NOT NULL,
  `tutored_subject` varchar(100) NOT NULL,
  `center` varchar(30) NOT NULL,
  `password` varchar(30) NOT NULL,
  `security_question` varchar(255) DEFAULT NULL,
  `security_answer` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `managers`
--

INSERT INTO `managers` (`id`, `email_id`, `name`, `tutored_subject`, `center`, `password`, `security_question`, `security_answer`) VALUES
(1, 'hastikundaria05@gmail.com', 'Hasti Kundaria', '', 'Ahmedabad', 'hasti1234', NULL, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `ratings`
--

CREATE TABLE `ratings` (
  `id` int(11) NOT NULL,
  `employee_id` int(11) NOT NULL,
  `manager_id` int(11) NOT NULL,
  `session_id` int(11) NOT NULL,
  `student_feedback` float NOT NULL,
  `task_efficiency` float NOT NULL,
  `engagement_level` float NOT NULL,
  `use_of_examples` float NOT NULL,
  `adaptability` float NOT NULL,
  `after_class_responsiveness` float NOT NULL,
  `confidence_boost` float NOT NULL,
  `final_score` float NOT NULL,
  `comments` text NOT NULL,
  `submitted_on` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `ratings`
--

INSERT INTO `ratings` (`id`, `employee_id`, `manager_id`, `session_id`, `student_feedback`, `task_efficiency`, `engagement_level`, `use_of_examples`, `adaptability`, `after_class_responsiveness`, `confidence_boost`, `final_score`, `comments`, `submitted_on`) VALUES
(3, 1, 1, 1, 4, 4.5, 4, 5, 3.8, 3, 4, 4.04, 'well experinced professor!', '2025-07-05 03:57:10'),
(4, 10, 1, 1, 5, 4, 3.8, 3.5, 4.5, 5, 4, 4.26, 'gives real life examples making learning new topics easier', '2025-08-07 19:36:44'),
(5, 10, 1, 1, 5, 5, 4, 4, 5, 5, 5, 4.71, 'awesome professor!', '2025-08-12 23:04:27');

-- --------------------------------------------------------

--
-- Table structure for table `review_sessions`
--

CREATE TABLE `review_sessions` (
  `id` int(10) NOT NULL,
  `start_date` date NOT NULL,
  `end_date` date NOT NULL,
  `is_active` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `review_sessions`
--

INSERT INTO `review_sessions` (`id`, `start_date`, `end_date`, `is_active`) VALUES
(6, '2025-07-03', '2025-08-02', 1),
(7, '2025-07-03', '2025-08-02', 1),
(8, '2025-07-04', '2025-08-03', 1),
(9, '2025-07-10', '2025-08-09', 1);

-- --------------------------------------------------------

--
-- Table structure for table `student`
--

CREATE TABLE `student` (
  `student_id` int(11) NOT NULL,
  `name` varchar(100) NOT NULL,
  `email` varchar(50) NOT NULL,
  `phone` varchar(20) NOT NULL,
  `course` varchar(255) DEFAULT NULL,
  `center` varchar(100) NOT NULL,
  `password` varchar(100) NOT NULL,
  `security_question` varchar(255) DEFAULT NULL,
  `security_answer` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `student`
--

INSERT INTO `student` (`student_id`, `name`, `email`, `phone`, `course`, `center`, `password`, `security_question`, `security_answer`) VALUES
(1, 'Nishi Barot', 'barotnishi9@gmail.com', '7324852510', 'Python, biology', 'Ahmedabad', 'Nishi1234', NULL, NULL),
(2, 'Krish Barot', 'krishbarot13@gmail.com', '4167174665', 'Python', 'Ahmedabad', 'krish1234', NULL, NULL),
(3, 'Vansh Barot', 'vanshbarot08@gmail.com', '6355392587', 'Python, Maths', 'Ahmedabad', 'vansh1234', NULL, NULL),
(4, 'Kahan Javeri', 'kahanjaveri1@gmail.com', '9856669752', 'Java, chemistry', 'ahmedabad', 'kahan1234', NULL, NULL),
(5, 'Divy Brambhatt', 'divybrambhatt1@gmail.com', '8482286762', 'Python, Biology, Java', 'Surat', 'Divy1234', 'What\'s your Mother\'s maiden name?', 'bebu');

-- --------------------------------------------------------

--
-- Table structure for table `student_feedback`
--

CREATE TABLE `student_feedback` (
  `id` int(11) NOT NULL,
  `student_id` int(11) NOT NULL,
  `employee_id` int(11) DEFAULT NULL,
  `rating` int(11) DEFAULT NULL,
  `comment` text DEFAULT NULL,
  `submitted_on` datetime DEFAULT NULL,
  `task_efficiency` float DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `student_feedback`
--

INSERT INTO `student_feedback` (`id`, `student_id`, `employee_id`, `rating`, `comment`, `submitted_on`, `task_efficiency`) VALUES
(1, 3, 1, 5, 'Feedback for Neil Barot', '2025-06-27 01:10:36', NULL),
(2, 3, 1, 5, 'test-1', '2025-06-27 01:28:38', NULL),
(3, 1, 1, 3, 'good professor, but speaks too fast', '2025-06-29 21:59:46', 4.6),
(4, 2, 1, 2, 'needs imporvement', '2025-07-01 00:21:40', 2.5),
(5, 3, 1, 4, 'test-2', '2025-07-01 00:25:14', 4.5),
(6, 4, 9, 4, 'teaches very well. sometimes over-explains stuff', '2025-07-03 23:55:50', 3.8),
(7, 4, 11, 3, 'i love the way he demonstrates equations. just not in basic language, sometimes gets complicated and hard to follow.', '2025-07-03 23:56:48', 4),
(8, 1, 10, 5, 'awesome professor!', '2025-08-12 23:04:27', 5);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `employee_personal`
--
ALTER TABLE `employee_personal`
  ADD PRIMARY KEY (`employee_id`);

--
-- Indexes for table `improvements`
--
ALTER TABLE `improvements`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `kpi_categories`
--
ALTER TABLE `kpi_categories`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `managers`
--
ALTER TABLE `managers`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `ratings`
--
ALTER TABLE `ratings`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `review_sessions`
--
ALTER TABLE `review_sessions`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `student`
--
ALTER TABLE `student`
  ADD PRIMARY KEY (`student_id`);

--
-- Indexes for table `student_feedback`
--
ALTER TABLE `student_feedback`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `employee_personal`
--
ALTER TABLE `employee_personal`
  MODIFY `employee_id` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;

--
-- AUTO_INCREMENT for table `improvements`
--
ALTER TABLE `improvements`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `kpi_categories`
--
ALTER TABLE `kpi_categories`
  MODIFY `id` int(10) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `managers`
--
ALTER TABLE `managers`
  MODIFY `id` int(50) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `ratings`
--
ALTER TABLE `ratings`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `review_sessions`
--
ALTER TABLE `review_sessions`
  MODIFY `id` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT for table `student`
--
ALTER TABLE `student`
  MODIFY `student_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `student_feedback`
--
ALTER TABLE `student_feedback`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
