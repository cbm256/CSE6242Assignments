package edu.gatech.cse6242;
import java.io.IOException;
import java.util.Iterator;
import java.util.StringTokenizer;
import java.util.List;
import java.lang.Object;
import java.util.ArrayList;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.io.*;
import org.apache.hadoop.mapreduce.*;
import org.apache.hadoop.util.*;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.input.SequenceFileInputFormat;
import org.apache.hadoop.mapreduce.task.JobContextImpl;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import org.apache.hadoop.mapreduce.lib.output.SequenceFileOutputFormat;

import org.apache.hadoop.mapreduce.Job;


public class Q4 {
    public static class TokenizerMapper
       extends Mapper<Object, Text, IntWritable, ArrayPrimitiveWritable>{
    private IntWritable sour = new IntWritable();
    private IntWritable targ = new IntWritable();

   public void map(Object key, Text value, Context context) throws IOException, InterruptedException  {
      StringTokenizer token =new StringTokenizer(value.toString(),"\t");
      sour.set(Integer.parseInt(token.nextToken()));
      targ.set(Integer.parseInt(token.nextToken()));
      context.write(sour,toArray(1,0));
      context.write(targ,toArray(0,1));
    }
    private ArrayPrimitiveWritable toArray(int v1, int v2){
        return new ArrayPrimitiveWritable( new int[]{v1, v2} );
    }
}


 public static class IntSumReducer
       extends Reducer<IntWritable,ArrayPrimitiveWritable,IntWritable,IntWritable> {
    //private IntWritable result = new IntWritable();

    public void reduce(IntWritable key, Iterable<ArrayPrimitiveWritable> values,
                       Context context
                       ) throws IOException, InterruptedException {
      Iterator<ArrayPrimitiveWritable> i = values.iterator();
      int count = 0;
      while ( i.hasNext() ){
          int[] counts = (int[])i.next().get();
          count += counts[0];
          count -= counts[1];
      }
      //result.set(count);
      context.write(key, new IntWritable(count));
    }
  }

    public static class TokenizerMapper1
       extends Mapper<Object, Text, IntWritable, IntWritable>{
    private final static IntWritable one = new IntWritable(1);
    private IntWritable source = new IntWritable();
    public void map(Object key, Text value, Context context) throws IOException, InterruptedException  {
    StringTokenizer tokens =new StringTokenizer(value.toString(),"\t");
    tokens.nextToken();
    source.set(Integer.parseInt(tokens.nextToken()));
    context.write(source,one);

    }
}

public static class IntSumReducer1
       extends Reducer<IntWritable,IntWritable,IntWritable,IntWritable> {
    private IntWritable result = new IntWritable();

    public void reduce(IntWritable key, Iterable<IntWritable> values,
                       Context context
                       ) throws IOException, InterruptedException {
      int sum = 0;
      for (IntWritable val : values) {
        sum += val.get();
      }
      result.set(sum);
      context.write(key, result);
    }
  }




  public static void main(String[] args) throws Exception {
    Configuration conf = new Configuration();
    Path out = new Path(args[1]);
    Job job1 = Job.getInstance(conf, "Q4");

    /* TODO: Needs to be implemented */

    job1.setJarByClass(Q4.class);
    job1.setMapperClass(TokenizerMapper.class);
    //job1.setCombinerClass(IntSumReducer.class);
    job1.setReducerClass(IntSumReducer.class);
    job1.setMapOutputKeyClass(IntWritable.class);
    job1.setMapOutputValueClass(ArrayPrimitiveWritable.class);
    job1.setOutputKeyClass(IntWritable.class);
    job1.setOutputValueClass(IntWritable.class);
    //job1.setOutputFormatClass(SequenceFileOutputFormat.class);
    FileInputFormat.addInputPath(job1, new Path(args[0]));
    FileOutputFormat.setOutputPath(job1, new Path(args[1] + "/output1"));

    job1.waitForCompletion(true);

    System.out.printf("Inside Job 2");
    Job job2 = Job.getInstance(conf, "sort by frequency");
    job2.setJarByClass(Q4.class);
    job2.setMapperClass(TokenizerMapper1.class);
    //job2.setNumReduceTasks(1);
    //job2.setCombinerClass(IntSumReducer1.class);
    job2.setReducerClass(IntSumReducer1.class);
    job2.setMapOutputKeyClass(IntWritable.class);
    job2.setMapOutputValueClass(IntWritable.class);
    job2.setOutputKeyClass(IntWritable.class);
    job2.setOutputValueClass(IntWritable.class);
    System.out.printf("Inside Job 2 at line 123");
    //job2.setInputFormatClass(SequenceFileInputFormat.class);
    FileInputFormat.addInputPath(job2, new Path(args[1] + "/output1"));
    FileOutputFormat.setOutputPath(job2, new Path(args[1] + "/output2"));
    System.out.printf("Inside Job 2 just before sys.exit");
    System.exit(job2.waitForCompletion(true) ? 0 : 1);

  }
}
