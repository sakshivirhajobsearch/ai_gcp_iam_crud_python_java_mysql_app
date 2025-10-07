package com.ai.gcp.iam.repository;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.util.ArrayList;
import java.util.List;

public class IAMRepository {

	public List<String> getAllUsers() throws Exception {
		
		List<String> users = new ArrayList<>();
		Connection conn = MySQLConnection.getConnection();
		PreparedStatement ps = conn.prepareStatement("SELECT email FROM iam_users");
		ResultSet rs = ps.executeQuery();
		while (rs.next()) {
			users.add(rs.getString("email"));
		}
		rs.close();
		ps.close();
		conn.close();
		return users;
	}

	public List<String> getAllAIAlerts() throws Exception {
		List<String> alerts = new ArrayList<>();
		Connection conn = MySQLConnection.getConnection();
		PreparedStatement ps = conn.prepareStatement("SELECT alert_text FROM iam_ai_alerts ORDER BY created_at DESC");
		ResultSet rs = ps.executeQuery();
		while (rs.next()) {
			alerts.add(rs.getString("alert_text"));
		}
		rs.close();
		ps.close();
		conn.close();
		return alerts;
	}
}
