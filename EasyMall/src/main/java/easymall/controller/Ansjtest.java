package easymall.controller;

import org.ansj.splitWord.analysis.ToAnalysis;

public class Ansjtest {
	public static void main(String[] args) {
		answer("这里是客服的回答内容");
	}
public static String answer(String texture) {
		
		String answer="这里是客服的回答内容";
		//String str=ToAnalysis.parse(answer).toString();
		String str=answer;
		int tag=0;
		char partall[]=new char[2000];
		int all=0;
		char partaqd[]=new char[2000];
		int aqd=0;
		char partvn[]=new char[2000];
		int vn=0;
		for(int i=0;i<str.length();i++) {
			tag=0;
			for(int l=i;l<str.length()&&(str.charAt(l))!=',';l++) {
				if(str.charAt(l)=='/')
				{
					if(tag==1) {
						partaqd[aqd++]=' ';
						partall[all++]=' ';
					}
						
					else if(tag==2) {
						partvn[vn++]=' ';
						partall[all++]=' ';
					}
					tag=10;
				}
				if(tag==10) {
					if(str.charAt(l)=='a'||str.charAt(l+1)=='q'||str.charAt(l)=='d')
						tag=1;
					else if(str.charAt(l)=='v'||str.charAt(l)=='n')
						tag=2;
				}
				else if(tag==1)	{
					partaqd[aqd++]=str.charAt(l);
					partall[all++]=str.charAt(l);
				}
				else if(tag==2) {
					partaqd[vn++]=str.charAt(l);
					partall[all++]=str.charAt(l);
				}
			}
		}
		for(int i=0;i<partall.length;i++)
			System.out.println(partall[i]);
		return answer;
	}
}
