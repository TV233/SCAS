package com.kclgroup.backend.mapper;

import com.kclgroup.backend.pojo.entity.IndexKlines;
import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.kclgroup.backend.pojo.vo.IndexKlineVo;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Select;

import java.util.List;

/**
* @author 张小明
* @description 针对表【index_klines】的数据库操作Mapper
* @createDate 2024-07-02 13:08:39
* @Entity com.kclgroup.backend.pojo.entity.IndexKlines
*/
@Mapper
public interface IndexKlinesMapper extends BaseMapper<IndexKlines> {

    @Select("select index_code,index_name,date_time,open,high,low,close,volume,value,last_close from index_klines where index_code = #{indexCode}")
    List<IndexKlineVo> getIndexKlines(String indexCode);
}




