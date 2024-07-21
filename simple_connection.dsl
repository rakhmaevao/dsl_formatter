# This container to other container
engee.blocks -> engee.code_processing "Исполняет julia код" "HTTP, Sockt.io" {
    tags "HTTP,Socket.io"
}
engee.blocks -> engee.state_api "Читает nglib" HTTP {
    tags "HTTP"
}

# This container to external component
engee.blocks -> engee.code_processing.code_preprocessor "Исполняет julia код" HTTP {
    tags "HTTP"
}
engee.blocks -> engee.code_processing.julia_kernel_listener "Ожидает результаты выполнения Julia кода" Socket.io {
    tags "Socket.io"
}

engee.blocks -> engee.state_api.ModelLoader "Читает nglib" HTTP {
    tags "HTTP"
}


# Internal component to other services
engee.blocks.mask_processor -> engee.code_processing "Исполняет julia код" HTTP {
    tags "HTTP"
}
engee.blocks.mask_processor -> engee.code_processing "Ожидает результаты выполнения Julia кода" Socket.io {
    tags "Socket.io"
}
engee.blocks.user_library_services -> engee.state_api "Читает nglib" {
    tags "HTTP"
}

# Internal component to internal component
engee.blocks.block_repr_builder -> engee.blocks.mask_processor "Пересчитать маску" 
engee.blocks.user_library_services -> engee.blocks.repositories "Запись сущностей" 
engee.blocks.GetNestedBlockLayoutService -> engee.blocks.repositories "Извлечение сущностей"  
engee.blocks.ConvertingDumpService -> engee.blocks.repositories "Извлечение сущностей"  
engee.blocks.ConvertingDumpService -> engee.blocks.block_repr_builder "Формирование BlockRepr"  
engee.blocks.library_services -> engee.blocks.repositories "Извлечение сущностей"  
engee.blocks.library_services -> engee.blocks.block_repr_builder "Формирование BlockRepr"  
engee.blocks.block_setup_services -> engee.blocks.repositories "Извлечение сущностей"  
engee.blocks.block_setup_services -> engee.blocks.block_repr_builder "Формирование BlockRepr"