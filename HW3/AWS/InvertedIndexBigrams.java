import java.io.IOException;
import java.util.HashMap;
import java.util.Iterator;
import java.util.Map;
import java.util.StringTokenizer;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.Reducer.Context;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;

public class InvertedIndexBigrams {
	
	public static class Mapping extends Mapper < Object, Text, Text, Text > {
		
	    private Text ID = new Text();
	    private Text Content = new Text();
	    public void map(Object key, Text value, Context context) throws IOException, InterruptedException {
	    	
	      String line = value.toString();
	 	  //line = line.replaceAll("[^a-zA-Z]", " ");
	      String[] separateWords = line.toString().split("\\t");
	      ID.set(separateWords[0]);
	      Content.set(separateWords[1].replaceAll("[^a-zA-Z]", " ").toLowerCase());
	      StringTokenizer iterator = new StringTokenizer(Content.toString());
	      String word1 = iterator.nextToken();
          while (iterator.hasMoreTokens())
          {
                  String word2 = iterator.nextToken();
                  String bigram = word1 + " " + word2;
                  context.write(new Text(bigram), new Text(ID));
                  word1 = word2;
          }
	    }    
	}
	
	  
	public static class Reducing extends Reducer < Text, Text, Text, Text > {
		  public void reduce(Text key, Iterable < Text > values, Context context) {
			 
		   HashMap <String, Integer> hash = new HashMap <String, Integer> ();
		   Iterator <Text> iterator = values.iterator();
		   int count = 0;
		   String id;
		   while (iterator.hasNext()) {
			   id = iterator.next().toString();
		    if (hash.containsKey(id)) {
		    	count = (hash.get(id));
		    	count += 1;
		     hash.put(id, count);
		    } else {
		    	hash.put(id, 1);
		    }

		   }
		   StringBuffer buffer = new StringBuffer("");
		   for (Map.Entry <String, Integer> mentry: hash.entrySet()) {
			   buffer.append(mentry.getKey() + ":" + mentry.getValue() + "\t");

		   }
		   try {
			context.write(key, new Text(buffer.toString()));
		} catch (Exception e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} 
	}
}


 public static void main(String[] args) throws Exception {
  Configuration conf = new Configuration();
  Job job = Job.getInstance(conf, "inverted index");
  job.setJarByClass(InvertedIndexBigrams.class);
  job.setMapperClass(Mapping.class);
 // job.setCombinerClass(Reducing.class);
  job.setReducerClass(Reducing.class);
  job.setOutputKeyClass(Text.class);
  job.setOutputValueClass(Text.class);
  FileInputFormat.addInputPath(job, new Path(args[0]));
  FileOutputFormat.setOutputPath(job, new Path(args[1]));
  System.exit(job.waitForCompletion(true) ? 0 : 1);
 }
}

