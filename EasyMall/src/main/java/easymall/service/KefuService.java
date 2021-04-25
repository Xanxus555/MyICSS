package easymall.service;





import java.util.List;

import easymall.po.Text;

public interface KefuService {
	public void sendtext(Text text);
	public List<Text> showtexture(int user_id);
}
