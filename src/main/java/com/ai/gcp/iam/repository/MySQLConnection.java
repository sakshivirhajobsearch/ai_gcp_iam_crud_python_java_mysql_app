package com.ai.gcp.iam.repository;

import java.sql.Connection;
import java.sql.DriverManager;

public class MySQLConnection {

	public static Connection getConnection() throws Exception {

		String url = "jdbc:mysql://localhost:3306/ai_gcp_iam?useSSL=false";
		String user = "root";
		String password = "admin";
		Class.forName("com.mysql.cj.jdbc.Driver");
		return DriverManager.getConnection(url, user, password);
	}
}
