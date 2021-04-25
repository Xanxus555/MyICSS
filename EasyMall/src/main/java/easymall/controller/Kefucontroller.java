package easymall.controller;


import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.sql.Timestamp;

import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.List;

import javax.servlet.http.HttpSession;

import org.ansj.splitWord.analysis.ToAnalysis;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.RequestMapping;

import easymall.po.Text;
import easymall.po.User;
import easymall.service.KefuService;


@Controller("KefuController")
@RequestMapping("/kefu")
public class Kefucontroller {
	@Autowired
	private KefuService KefuService;
	@RequestMapping("/showtexture")
	public String showcart(HttpSession session,Model model) {
		User user=(User)session.getAttribute("user");
		List<Text> texts=KefuService.showtexture(user.getId());
		/*for(Text s:texts) {
			System.out.println(""+s.getUser_id()+s.getTexttime()+s.getText());
		}
		*/
		
		model.addAttribute("msg",texts);
		
		return "kefu";
	}
	@RequestMapping("/tokefu")
	public String speaker() {
		return "kefu";
	}
	@RequestMapping("/sendtext")
	public String sendtexture(HttpSession session,String texture) {
		//System.out.println(texture);
		
		User user=(User)session.getAttribute("user");
		SimpleDateFormat df=new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");
		String time=df.format(new Date());
		Timestamp timeStamp=Timestamp.valueOf(time);

		Text text=new Text(user.getId(),1,timeStamp,texture);

		KefuService.sendtext(text);
		
		Date now=new Date();
		now.setTime(now.getTime()+1000);
		String time2=df.format(now);
		Timestamp timeStamp2=Timestamp.valueOf(time2);
		
		Text text2=new Text(1,user.getId(),timeStamp2,answer(texture));
		KefuService.sendtext(text2);
		return "forward:/kefu/showtexture";
	}
	public static String answer(String texture) {
		
		String answer="这里是客服的回答内容";
		String str=ToAnalysis.parse(texture).toString();
		System.out.println(str);
		char partall[]=new char[250];
		int all=0;
		char partaqd[]=new char[250];
		int aqd=0;
		char partvn[]=new char[250];
		int vn=0;

		for(int i=0;i<str.length();i++) {
				if(str.charAt(i)=='/')
				{
					int l=i;
					if(str.charAt(l+1)=='a'||str.charAt(l+1)=='q'||str.charAt(l+1)=='d') {
						for(;l>=0&&str.charAt(l)!=',';l--);
						
						for(l++;l<str.length()&&str.charAt(l)!='/';l++) {
							partaqd[aqd++]=str.charAt(l);
							partall[all++]=str.charAt(l);
						}
						partaqd[aqd++]=' ';
						partall[all++]=' ';
					}
					
					else if(str.charAt(l+1)=='v'||str.charAt(l+1)=='n') {
						for(;l>=0&&str.charAt(l)!=',';l--);
						for(l=l+1;l<str.length()&&str.charAt(l)!='/';l++) {System.out.println(str.charAt(l));
							partvn[vn++]=str.charAt(l);
							partall[all++]=str.charAt(l);
						}
						partvn[vn++]=' ';
						partall[all++]=' ';
					}
				}
			}
		for(int i=0;i<partall.length;i++) {
			System.out.println("第"+i+"个字符：");
			System.out.println(partall[i]);
		
		}
//		String[] arguments = new String[] {"python", "D:\\作业\\java\\ICSS\\ICSS\\Main\\main.py",partvn, partaqd, partall};
//
        try {
//
//            Process process = Runtime.getRuntime().exec(arguments);
//
//            BufferedReader in = new BufferedReader(new InputStreamReader(process.getInputStream()));
//
//            String line = null;
//
//          while ((line = in.readLine()) != null) {  
//
//              System.out.println(line);  
//              answer = line;
//          }  
        	String sysPython = "python.exe ";
			String filePython = " D:\\作业\\java\\ICSS\\EasyMall\\src\\main\\java\\\\easymall\\controller\\main.py ";
	        Process proc = Runtime.getRuntime().exec(sysPython + filePython + partvn + partaqd + partall);// 执行py文件
	        BufferedReader in = new BufferedReader(new InputStreamReader(proc.getInputStream()));
	        String line = null;
	        while ((line = in.readLine()) != null) {
	            answer = line;
	            System.out.println(line);
	        }
	        System.out.println("输出成功");
	        in.close();
	        System.out.println(proc.waitFor());
        }catch (Exception e) {
        	e.printStackTrace();
		}
          //java代码中的process.waitFor()返回值为0表示我们调用python脚本成功，

            //返回值为1表示调用python脚本失败，这和我们通常意义上见到的0与1定义正好相反
		return answer;
	}
}
