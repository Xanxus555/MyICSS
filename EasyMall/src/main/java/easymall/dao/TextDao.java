package easymall.dao;

import java.util.List;
import org.apache.ibatis.annotations.Mapper;
import org.springframework.stereotype.Repository;

import easymall.po.Text;

@Repository("textDao")
@Mapper
public interface TextDao {
	public List<Text> showtexture(int user_id);
	public void sendtext(Text text);
}