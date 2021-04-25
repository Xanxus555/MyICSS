package easymall.service;



import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;



import easymall.dao.TextDao;
import easymall.po.Text;

@Service("kefuService")
public class KefuServiceImpl implements KefuService{
	@Autowired
	private TextDao textDao;
	@Override
	public void sendtext(Text text) {
		textDao.sendtext(text);
	}
	@Override
	public List<Text> showtexture(int user_id){
		return textDao.showtexture(user_id);
	}
}
