-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Aug 11, 2025 at 09:03 PM
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
-- Table structure for table `delivery`
--

CREATE TABLE `delivery` (
  `id` int(11) NOT NULL,
  `category` varchar(100) NOT NULL,
  `product_name` varchar(255) NOT NULL,
  `product_quantity` int(11) NOT NULL,
  `price` decimal(10,2) NOT NULL,
  `total_price` decimal(12,2) GENERATED ALWAYS AS (`product_quantity` * `price`) STORED,
  `paid` decimal(10,2) DEFAULT 0.00,
  `due` decimal(10,2) GENERATED ALWAYS AS (`total_price` - `paid`) STORED,
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
  `price` decimal(10,2) NOT NULL,
  `stored_in` varchar(255) DEFAULT NULL,
  `stock` int(11) DEFAULT 0,
  `sold` int(11) DEFAULT 0,
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
(1, 'Computers & Laptops', 'Macbook air', 'Apache', 'Black, Green, Yellow', 'test descrptions', 23450.00, '122 location', 333, 5656, 'Xianung', '+8443444674', 'zisimpung', 'images/products/computers-laptops/monitor1.jpg', 'images/products/computers-laptops/2021-637571985004009642-400.jpg', 'images/products/computers-laptops/pc4.jpg', 'images/products/computers-laptops/mhn23.mp4', '2025-08-10', '2025-08-10 09:34:51', '2025-08-11 16:22:56'),
(2, 'Computers & Laptops', 'dell laptop', 'Not applicable', 'White, Blue, Red, Perple', 'google img descri', 89.00, '', 258294, 92773, 'Guanzhu', '+4529097732', 'Xuangvung', 'images/products/computers-laptops/deco.jpg', 'images/products/computers-laptops/laptop1.jpg', NULL, NULL, '2025-08-10', '2025-08-10 10:00:12', '2025-08-11 16:23:22'),
(3, 'Fashion & Wear', 'Man forman dress Court and pant and tie', 'Ducati', 'Not aplicable', 'About this item\r\nPrintable cardstock lets you design and print your own personalized business cards\r\nOur most premium business cards feature Clean Edge(R) technology so that cards snap apart easily and leave behind the smoothest cleanest edges of any printable business card available\r\nOptimized for inkjet printers for jam & smudge-free performance guaranteed. Add crisp text and vibrant images to both sides of the professional business cards.\r\nPersonalize your white business card with your own design or choose from thousands of free templates and designs on the Avery site\r\nIdeal for professional-quality printable business cards gift cards gift tags coupons or customer loyalty cards; use the back for photos maps and notes\r\n   Report an issue with this product or seller', 8393.00, '', 4892391, 287892, 'Kunming', '+834710923', 'Kungxing', 'images/products/fashion-wear/general-1.png', 'images/products/fashion-wear/MEN_S_BUSINESS_CASUAL_ATTIRE_1.jpg', 'images/products/fashion-wear/Untitled_design_39_800x.webp', 'images/products/fashion-wear/de.mp4', '2025-08-10', '2025-08-10 10:05:21', '2025-08-11 16:23:34');

-- --------------------------------------------------------

--
-- Table structure for table `orders`
--

CREATE TABLE `orders` (
  `id` int(11) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `product_id` int(11) DEFAULT NULL,
  `quantity` int(11) DEFAULT NULL,
  `total_price` decimal(10,2) DEFAULT NULL,
  `order_date` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `name` varchar(100) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `password` varchar(255) DEFAULT NULL,
  `role` enum('admin','vendor','customer') DEFAULT 'customer',
  `shop_name` varchar(150) DEFAULT NULL,
  `address` text DEFAULT NULL,
  `nid_or_passport_number` varchar(50) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Indexes for dumped tables
--

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
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`),
  ADD KEY `product_id` (`product_id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`);

--
-- AUTO_INCREMENT for dumped tables
--

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
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `orders`
--
ALTER TABLE `orders`
  ADD CONSTRAINT `orders_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
  ADD CONSTRAINT `orders_ibfk_2` FOREIGN KEY (`product_id`) REFERENCES `products` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
