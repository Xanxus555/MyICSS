package easymall.po;

import java.sql.Timestamp;

public class Text {
	private Integer user_id;
	private Integer getter_id;
	private Timestamp texttime ;
	private String text;

	public Integer getUser_id() {
		return user_id;
	}
	public void setUser_id(Integer user_id) {
		this.user_id = user_id;
	}
	public Timestamp getTexttime() {
		return texttime;
	}
	public void setTexttime(Timestamp texttime) {
		this.texttime = texttime;
	}
	public String getText() {
		return text;
	}
	public void setText(String text) {
		this.text = text;
	}
	public Text(Integer user_id,Integer getter_id, Timestamp texttime, String text) {
		this.getter_id=getter_id;
		this.user_id = user_id;
		this.texttime = texttime;
		this.text = text;
	}
	public Text() {

	}
	
}
