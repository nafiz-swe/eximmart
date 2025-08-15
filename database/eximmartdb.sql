-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Aug 15, 2025 at 02:11 PM
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
-- Database: `eximmartdb`
--

-- --------------------------------------------------------

--
-- Table structure for table `cart`
--

CREATE TABLE `cart` (
  `cart_id` int(11) NOT NULL,
  `users_id` int(11) NOT NULL,
  `users_mobile` varchar(50) NOT NULL,
  `product_id` int(11) NOT NULL,
  `product_name` varchar(255) NOT NULL,
  `unit_price` int(25) NOT NULL,
  `quantity` int(25) NOT NULL DEFAULT 1,
  `total_price` int(25) NOT NULL,
  `added_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `cart`
--

INSERT INTO `cart` (`cart_id`, `users_id`, `users_mobile`, `product_id`, `product_name`, `unit_price`, `quantity`, `total_price`, `added_at`) VALUES
(5, 1, '01737226404', 3, 'Man forman dress Court and pant and tie', 8393, 150, 1258950, '2025-08-15 12:09:50'),
(7, 1, '01737226404', 2, 'dell laptop', 89, 258294, 22988166, '2025-08-12 09:37:53'),
(8, 1, '01737226404', 1, 'Macbook air', 23450, 69, 1618050, '2025-08-15 11:32:53');

-- --------------------------------------------------------

--
-- Table structure for table `delivery`
--

CREATE TABLE `delivery` (
  `id` int(11) NOT NULL,
  `category` varchar(100) NOT NULL,
  `product_name` varchar(255) NOT NULL,
  `product_quantity` int(25) NOT NULL,
  `price` int(25) NOT NULL,
  `total_price` int(25) GENERATED ALWAYS AS (`product_quantity` * `price`) STORED,
  `paid` int(25) DEFAULT 0,
  `due` int(25) GENERATED ALWAYS AS (`total_price` - `paid`) STORED,
  `user_name` varchar(150) NOT NULL,
  `user_contact_number` varchar(20) NOT NULL,
  `user_email` varchar(150) DEFAULT NULL,
  `delivery_address` text NOT NULL,
  `delivery_status` enum('Pending','Shipped','Delivered','Cancelled') DEFAULT 'Pending',
  `export_date` date NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `imported_products`
--

CREATE TABLE `imported_products` (
  `id` int(11) NOT NULL,
  `category` varchar(100) NOT NULL,
  `product_name` varchar(255) NOT NULL,
  `brand_name` varchar(255) DEFAULT NULL,
  `product_color` varchar(100) DEFAULT NULL,
  `description` text DEFAULT NULL,
  `price` int(25) NOT NULL,
  `stored_in` varchar(255) DEFAULT NULL,
  `stock` int(25) DEFAULT 0,
  `sold` int(25) DEFAULT 0,
  `factory_shop_address` varchar(255) DEFAULT NULL,
  `contact_number` varchar(20) DEFAULT NULL,
  `product_owner_name` varchar(255) DEFAULT NULL,
  `product_image1` varchar(255) DEFAULT NULL,
  `product_image2` varchar(255) DEFAULT NULL,
  `product_image3` varchar(255) DEFAULT NULL,
  `product_video` varchar(255) DEFAULT NULL,
  `import_date` date DEFAULT curdate(),
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `imported_products`
--

INSERT INTO `imported_products` (`id`, `category`, `product_name`, `brand_name`, `product_color`, `description`, `price`, `stored_in`, `stock`, `sold`, `factory_shop_address`, `contact_number`, `product_owner_name`, `product_image1`, `product_image2`, `product_image3`, `product_video`, `import_date`, `created_at`, `updated_at`) VALUES
(1, 'Computer & Laptop', 'Macbook air', 'Apache', 'Black, Green, Yellow', 'test descrptions', 23450, '122 location', 333, 5656, 'Xianung', '+8443444674', 'zisimpung', 'images/products/computers-laptops/monitor1.jpg', 'images/products/computers-laptops/2021-637571985004009642-400.jpg', 'images/products/computers-laptops/pc4.jpg', 'images/products/computers-laptops/mhn23.mp4', '2025-08-10', '2025-08-10 09:34:51', '2025-08-12 14:54:22'),
(2, 'Computer & Laptop', 'dell laptop', 'Not applicable', 'White, Blue, Red, Perple', 'google img descri', 89, '', 258294, 92773, 'Guanzhu', '+4529097732', 'Xuangvung', 'images/products/computers-laptops/deco.jpg', 'images/products/computers-laptops/laptop1.jpg', NULL, NULL, '2025-08-10', '2025-08-10 10:00:12', '2025-08-12 15:00:54'),
(3, 'Fashion & Wear', 'Man forman dress Court and pant and tie', 'Ducati', 'Not aplicable', 'About this item\r\nPrintable cardstock lets you design and print your own personalized business cards\r\nOur most premium business cards feature Clean Edge(R) technology so that cards snap apart easily and leave behind the smoothest cleanest edges of any printable business card available\r\nOptimized for inkjet printers for jam & smudge-free performance guaranteed. Add crisp text and vibrant images to both sides of the professional business cards.\r\nPersonalize your white business card with your own design or choose from thousands of free templates and designs on the Avery site\r\nIdeal for professional-quality printable business cards gift cards gift tags coupons or customer loyalty cards; use the back for photos maps and notes\r\n   Report an issue with this product or seller', 8393, '', 4892391, 287892, 'Kunming', '+834710923', 'Kungxing', 'images/products/fashion-wear/general-1.png', 'images/products/fashion-wear/MEN_S_BUSINESS_CASUAL_ATTIRE_1.jpg', 'images/products/fashion-wear/Untitled_design_39_800x.webp', 'images/products/fashion-wear/de.mp4', '2025-08-10', '2025-08-10 10:05:21', '2025-08-11 16:23:34');

-- --------------------------------------------------------

--
-- Table structure for table `orders`
--

CREATE TABLE `orders` (
  `id` int(11) UNSIGNED NOT NULL,
  `user_name` varchar(150) NOT NULL,
  `user_email` varchar(255) NOT NULL,
  `user_mobile` varchar(50) NOT NULL,
  `shipping_address` text NOT NULL,
  `id_proof_type` enum('nid','passport','') NOT NULL DEFAULT '',
  `id_number` varchar(100) DEFAULT NULL,
  `id_file_path` varchar(255) DEFAULT NULL,
  `payment_method` enum('bkash','rocket','cash_on_delivery','card') NOT NULL,
  `total_categories` int(11) DEFAULT 0,
  `total_quantity` int(25) DEFAULT 0,
  `total_price` int(25) DEFAULT 0,
  `order_status` enum('pending','processing','product_at_courier','product_at_warehouse','ready_for_delivery','received') NOT NULL DEFAULT 'pending',
  `order_date` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `orders`
--

INSERT INTO `orders` (`id`, `user_name`, `user_email`, `user_mobile`, `shipping_address`, `id_proof_type`, `id_number`, `id_file_path`, `payment_method`, `total_categories`, `total_quantity`, `total_price`, `order_status`, `order_date`) VALUES
(1, 'Nafizul Islam', 'nafizulislam.swe@gmail.com', '01737226404', 'Bahimali, Baraigram, Harowa', 'nid', '4204957320', 'images/orders/20250812083258_NID.jpg', 'bkash', 3, 37901, 819105532, 'product_at_warehouse', '2025-08-12 08:32:58');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(11) UNSIGNED NOT NULL,
  `users_name` varchar(150) NOT NULL,
  `users_email` varchar(255) NOT NULL,
  `users_mobile` varchar(50) NOT NULL,
  `users_profession` varchar(100) NOT NULL,
  `users_password` varchar(255) NOT NULL,
  `users_create_account` timestamp NOT NULL DEFAULT current_timestamp(),
  `users_update_account` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `users_name`, `users_email`, `users_mobile`, `users_profession`, `users_password`, `users_create_account`, `users_update_account`) VALUES
(1, 'Nafizul Islam', 'nafizulislam.swe@gmail.com', '01737226404', 'Student', 'scrypt:32768:8:1$VGqdJYDBLlixRnoA$4946d17e9651459b7f068d0747c849dd51c0a8539f4eb3d506eb3e5eb5f0381c1f42e195b4d72b0ed75467773f65929f383a660e79e5ee6b6d4c0a1f8404706b', '2025-08-12 07:43:15', '2025-08-12 07:43:15');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `cart`
--
ALTER TABLE `cart`
  ADD PRIMARY KEY (`cart_id`),
  ADD UNIQUE KEY `user_product_unique` (`users_id`,`product_id`);

--
-- Indexes for table `delivery`
--
ALTER TABLE `delivery`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `imported_products`
--
ALTER TABLE `imported_products`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `orders`
--
ALTER TABLE `orders`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `users_email` (`users_email`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `cart`
--
ALTER TABLE `cart`
  MODIFY `cart_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT for table `delivery`
--
ALTER TABLE `delivery`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `imported_products`
--
ALTER TABLE `imported_products`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `orders`
--
ALTER TABLE `orders`
  MODIFY `id` int(11) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
