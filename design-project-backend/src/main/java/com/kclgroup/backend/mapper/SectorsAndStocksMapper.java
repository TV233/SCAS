package com.kclgroup.backend.mapper;

import com.kclgroup.backend.pojo.entity.SectorsAndStocks;
import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Select;

import java.util.List;

/**
* @author 张小明
* @description 针对表【sectors_and_stocks】的数据库操作Mapper
* @createDate 2024-06-24 20:57:12
* @Entity com.kclgroup.backend.pojo.entity.SectorsAndStocks
*/
@Mapper
public interface SectorsAndStocksMapper extends BaseMapper<SectorsAndStocks> {
    @Select("SELECT * FROM sectors_and_stocks")
    List<SectorsAndStocks> getSectorsAndStocks();
}




